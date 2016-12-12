# pylint-oops-overrides
Avoid non-expected method overrides in your Python code.

## What is the problem?
Sometimes you codebase grows a lot and you go ahead and start
implementing some new feature. You extend some class of the framework
you are using like `django.models.Model` and everything is fine. Then
for some reason your application starts behaving strange and you have
no idea why. After weeks of headache you realise that the problem was
that you override by mistake one of the internal
`django.models.Model`'s methods.

This situation was actually described by a friend of mine
[@arthuralvim](https://github.com/arthuralvim) to me and kept me
thinking how we could avoid this to happen again. At the moment that
we talked I just thought about good testing coverage and integration
tests. But I thought maybe there is another way, but probably very
complex to implement something that checks for this mistaken overrides
automatically. I left it alone and moved on.

Later the same day I was reading an article with some sample code in
Java. There I could see the annotation `@Overrides` immediately I
thought:

> "OH! That could be used to mark safe overrides. I could create a
> plugin to pylint to check methods overridden methods if they were
> implemented consciously or not.

The result is this small "oops-overrides" pylint checker.

## How it works?
The `oops-overrides-checker` checks if all methods overridden from
classes defined in external libraries in your code to have a decorator
called "overrides". Example:

``` python
from unittest.mock import MagicMock


class MyConsciousOverride(MagicMock):
    @overrides
    def assert_any_call(self, *args, **kwargs):
        """
        This one should not show any error since I marked it as a safe
        override.
        """
        print('conscious override!')
```
