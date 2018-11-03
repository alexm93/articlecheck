import operator
from functools import reduce


class CalculationError(Exception):

    def __init__(self, message):
        self.message = message


class Error:

    ERRORS_MAP = {
        "text_content_contains": "Текст не содержит {}.",
        "text_content_not_contains": "Текст содержит {}.",
        "text_length_less": "Текст больше {} символов.",
        "text_length_more": "Текст меньше {} символов.",
        "text_length_equal": "В тексте не {} символов.",
        "category_title_equal": "Категория не {}.",
        "category_title_in": "Категория не содержится в {}.",
        "category_title_not_in": "Категория содержится в {}."
    }

    def __init__(self, rule):
        self._rule = rule
        self._desc = self._get_error_desc()

    def _get_error_desc(self):
        error = ""
        if not self._rule.result:
            error = self.ERRORS_MAP["_".join([self._rule.obj,
                                              self._rule.prop, self._rule.expression])].format(self._rule.value)
        return error

    def __str__(self):
        return self._desc


class Rule:

    OBJECT = {
        "text": lambda article: article,
        "category": lambda article: "Новости"
    }

    PROPERTY = {
        "content": lambda obj: obj,
        "length": lambda obj: len(obj),
        "title": lambda obj: obj
    }

    EXPRESSION = {
        "contains": operator.contains,
        "not_contains": lambda prop, val: not operator.contains(prop, val),
        "more": operator.gt,
        "less": operator.lt,
        "equal": operator.eq,
        "in": lambda prop, val: operator.contains(val, prop),
        "not_in": lambda prop, val: not operator.contains(val, prop)
    }

    AVAILABLE_OBJ_PROP_EXPR_COMBINATIONS = Error.ERRORS_MAP.keys()

    def __init__(self, article, object, property, expression, value):
        self._article = article
        self._obj = object
        self._prop = property
        self._expression = expression
        self._value = value
        self._result = self._get_result()

    def _get_result(self):
        if not "_".join([self._obj, self._prop, self._expression]) in self.AVAILABLE_OBJ_PROP_EXPR_COMBINATIONS:
            raise CalculationError(message="Wrong rule. Not available object, property, expression combination.")
        obj = self.OBJECT[self._obj](self._article)
        prop = self.PROPERTY[self._prop](obj)
        expression = self.EXPRESSION[self._expression]
        try:
            result = expression(prop, self._value)
        except (ValueError, TypeError):
            raise CalculationError(message="Wrong rule. Calculation error. Bad value.")
        return result

    @property
    def obj(self):
        return self._obj

    @property
    def prop(self):
        return self._prop

    @property
    def expression(self):
        return self._expression

    @property
    def value(self):
        return self._value

    @property
    def result(self):
        return self._result

    def get_verbose_result(self):
        return {
            "is_valid": self._result,
            "error": str(Error(self))
        }

    def get_logic_expr(self):
        return "{} {} {} {}".format(self._obj, self._prop, self._expression, self._value)


class Group:

    OPERATOR = {
        "or": lambda x, y: x or y,
        "and": lambda x, y: x and y
    }

    def __init__(self, article, operator, rules=None, groups=None):
        self._article = article
        self._operator = operator
        self._rules = self._create_rules(rules)
        self._groups = self._create_groups(groups)
        self._result = self._get_result()

    def _create_rules(self, rules):
        return [Rule(self._article, **rule) for rule in rules] if rules else None

    def _create_groups(self, groups):
        return [Group(self._article, **group) for group in groups] if groups else None

    def _get_result(self):
        operator = self.OPERATOR[self._operator]
        rules_res = [rule.result for rule in self._rules] if self._rules else [True]
        group_res = [group.result for group in self._groups] if self._groups else [True]
        return reduce(operator, rules_res + group_res)

    @property
    def result(self):
        return self._result

    def get_verbose_result(self):
        result = {"is_valid": self._result}
        if self._rules:
            result["rules"] = [rule.get_verbose_result() for rule in self._rules]
        if self._groups:
            result["groups"] = [group.get_verbose_result() for group in self._groups]
        return result

    def get_logic_expr(self):
        rules_expr = "\n{}\n".format(self._operator.upper()).join(
            rule.get_logic_expr() for rule in self._rules) if self._rules else None
        groups_expr = "\n{}\n".format(self._operator.upper()).join(
            group.get_logic_expr() for group in self._groups) if self._groups else None
        if rules_expr and groups_expr:
            return "({}\n{}\n{})".format(rules_expr, self._operator.upper(), groups_expr)
        else:
            return "({})".format(rules_expr or groups_expr)
