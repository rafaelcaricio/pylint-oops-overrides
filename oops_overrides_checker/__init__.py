from pylint.checkers import BaseChecker, utils
from pylint.interfaces import IAstroidChecker
import importlib
import inspect


class MethodOverridesChecker(BaseChecker):
    __implements__ = (IAstroidChecker,)

    name = 'Checks for non-safe overrides'
    MESSAGE_ID = 'oops-non-safe-override'
    msgs = {
        'E9940': (
            "Method %s.%s is not marked as a safe override.",
            MESSAGE_ID,
            "Used whee classes.",
        ),
    }

    @utils.check_messages(MESSAGE_ID)
    def visit_functiondef(self, node):
        if node.is_method():
            class_def = node.parent.frame()
            bases = class_def.bases
            method_decorators = []
            if node.decorators is not None:
                for decorator in node.decorators.nodes:
                    method_decorators.append(decorator.name)

            # look in every base class for overrides (for base_class in class_def.bases:)
            external_base_class = bases[0].name
            package = node.lookup(external_base_class)[1][0].modname
            # check if it is not an internal import
            # use importlib to import the module
            external_class = getattr(importlib.import_module(package), external_base_class, None)
            if external_class:
                # check the methods defined in the class.__dict__ if
                # the name is present, if true, it is a override
                if node.name in dict(inspect.getmembers(external_class)).keys():
                    if 'overrides' not in method_decorators:
                        self.add_message(
                            self.MESSAGE_ID, args=(class_def.name, node.name), node=node)


def register(linter):
    linter.register_checker(MethodOverridesChecker(linter))
