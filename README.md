# pylint-oops-overrides
Avoid non-expected method overrides in your Python code.

## What is the problem?
Codebases grows and new features are always waiting to be added. In
certain situations you need to extend some class of the framework you
are using like `django.db.models.Model` to implement some feature. You
write some tests and everything seems fine. You deploy to production
and something seems strange. In some specific corner case, that you
missed in the tests, the code is not working as expected. You have no
idea why. After weeks of investigation and headache you realise that
the problem was that you have overridden by mistake one of the internal
`django.db.models.Model`'s methods. Oops!

This situation was actually described by a friend of mine
[@arthuralvim](https://github.com/arthuralvim) to me and kept me
thinking how we could avoid this to happen in Python where everything
is dynamic (and it is a good thing!). At the moment that we talked I
thought about good testing coverage and integration tests. I also I
thought that maybe there is another way, but probably very complex to
implement something that checks for this mistaken overrides
automatically. So I left it alone and moved on.

Later in the same day I was reading an article with some code sample in
Java and there I could see the annotation `@Overrides`. Immediately I
thought:

> "OH, wait! I could use something like that in Python to mark safe
> overrides. Additionally, I could create a plugin to pylint to look
> for overridden methods if they were implemented consciously
> (explicitly marked as a override) or not.

The result is this small "oops-overrides" pylint checker.

## How it works?
The `oops-overrides-checker` looks for all methods you override from
external libraries and verify if they have a decorator called
"overrides".

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

The example above will not generate any errors from
`oops-overrides-checker` since the method `assert_any_call` is
properly marked as a safe override.

``` python
class MyNaiveOverride(MagicMock):
    def assert_any_call(self, *args, **kwargs):
        """
        Overrides without any marker.
        """
        print('Naive override')
```

In this second example `oops-overrides-checker` will display an error output like:

``` shell
$ pylint -E --load-plugins oops_overrides_checker tests/fixtures/my_naive_code.py
************* Module my_naive_code
E: 11, 4: Method MyNaiveOverride.assert_any_call is not marked as a safe override. (oops-non-safe-override)
```

In case you override by mistake some internal methods of the
frameworks/libraries you use you know where potential errors might
exist.

## Where to use?
We recommend you to use `oops-overrides-checker` in you CI system and
continously watch out for potential overseen method overrides.

## Possible integrations
You might use `oops-overrides-checker` pylint plugin in conjunction
with [`overrides`](https://github.com/mkorpela/overrides). Overrides
is a decorator to automatically detect mismatch when overriding a
methods. It executes in runtime with your code and checks if your
implementation is compliant with the original method definition.
