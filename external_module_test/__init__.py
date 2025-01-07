from grimoiressg.modules import available_modules


def test(data, context):
    print("This is test module.")


available_modules["test"] = test
