class Cat:
    def __init__(self, name, color):
        self.__name = name
        self.__color = color

    def meow(self):
        print("meow")

    def get_color(self):
        return self.__color

    def set_color(self, color):
        self.__color = color

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__color = name

    def del_name(self):
        del self.__name

    color = property(get_color, set_color)
    name = property(get_name, set_name, del_name)

class Cat2:
    def __init__(self, name, color):
        self.__name = name
        self.__color = color

    def meow(self):
        print("meow")

    def get_color(self):
        return self.__color

    def set_color(self, color):
        self.__color = color

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__color = name

def num_of_properties_with_deletion(cl):
    i = 0
    for key in cl.__dict__:
        ev_attr = getattr(cl, key)
        cl_name = ev_attr.__class__.__name__
        if cl_name == "property":
            if ev_attr.fdel is not None:
                i += 1
    print("properties with deletion:", i, " in class", cl.__name__)


if __name__ == '__main__':
    cat = Cat("Snowball", "red")
    cat2 = Cat2("Max", "white")
    num_of_properties_with_deletion(Cat)
    num_of_properties_with_deletion(Cat2)





# def tracer(func):
#     def wrapper(*args):
#         wrapper.calls += 1
#         print("in ", wrapper.calls)
#         func(*args)
#     wrapper.calls = 0
#     return wrapper
#
#
# class A:
#     a = int()
#     def __init__(self, na):
#         print("init")
#         self.a = na
#
#     @tracer
#     def get_a(self):
#         return self.a
#
#     @tracer
#     def set_a(self, na):
#         self.a = na
#
#     def del_a(self):
#         del self.a
#
#
# class Dec:
#     def __init__(self, func):
#         self.func =func
#
#     def __call__(self, *args, **kwargs):
#         print("call dec")
#         i = 1
#         for a in args:
#             print(i, a, sep=') ')
#         print(kwargs)
#         self.func(*args)
#
#     def __get__(self, instance, owner):
#         print("get")
#         return Wrapper(self, instance)
#
# class Wrapper:
#     def __init__(self, dec, cl_obj):
#         print("wrap init")
#         self.dec = dec
#         self.cl_obj = cl_obj
#
#
#     def __call__(self, *args, **kwargs):
#         print("call wrap")
#         return self.dec(self.cl_obj, *args, **kwargs)
#
#
#
# class Class:
#     @Dec
#     def sum(self, *args):
#         i = 1
#         for a in args:
#             print(i, a, sep=')) ')
#             i += 1
#
# @Dec
# def sum(*args):
#     i = 1
#     for a in args:
#         print(i, a, sep=')) ')
#         i += 1



# class Descriptor:
#     def __init__(self):
#         self.calls = 0
#
#     def __get__(self, instance, owner):
#         self.calls += 1
#         print("instance = ", instance)
#         print("owner = ", owner)
#         return self.color
#
#     def __set__(self, instance, value):
#          self.color = value
#
#     def __delete__(self, instance):
#         del self.color


# class Wrapper:
#     def __init__(self, desc, cl):
#         self.desc = desc
#         self.cl = cl
#
#     def __call__(self, *args, **kwargs):
#         return self.desc(self.cl, *args, *kwargs)
#
# class CatVoice:
#     def __init__(self, func):
#         self.count = 0
#         self.func = func
#
#     def __call__(self, *args, **kwargs):
#         self.count += 1
#         self.func(*args)
#
#     def __get__(self, instance, owner):
#         return Wrapper(self, instance)
#
#
# class Meta(type):
#     def __new__(mcs, *args, **kwargs):
#         p = args[2]
#         print(p['meow'])
#         c = type.__new__(mcs, args, kwargs)
#         c.__setattr__("spy", "hhh")
#         return c
#
#
# class Cat(metaclass=Meta):
#     color = Descriptor()
#     def __init__(self, name, color):
#         self.name = name
#         self.color = color
#
#     def meow(self):
#         print("meow")










