import unittest

from tori.decorator.common import *

class TestDecoratorCommonSingletonClass(unittest.TestCase):
    """ Test the 'singleton' decorator. """
    class DummyTest(object):
        def __init__(self):
            self.number = 0
        def take_action(self):
            self.number += 1
        def get_number(self):
            return self.number
    
    def test_positive_without_instance_attr(self):
        """ Test if the target class without a singleton attribute. """
        try:
            @singleton
            class SuperDummyClass(TestDecoratorCommonSingletonClass.DummyTest): pass
            self.assertTrue(True, 'Singleton Class: Passed the initialization as expected.')
        except SingletonInitializationException:
            self.assertTrue(False, 'Singleton Class: Failed the initialization with known exception.')
        
        # Test for the type.
        self.assertIsInstance(SuperDummyClass.instance(), SuperDummyClass)
        # Test if it is working. (case #1)
        SuperDummyClass.instance().take_action()
        self.assertEqual(SuperDummyClass.instance().get_number(), 1)
        # Test if it is working. (case #n)
        SuperDummyClass.instance().take_action()
        self.assertEqual(SuperDummyClass.instance().get_number(), 2)
    
    def test_positive_using_decorator_with_primitive_parameters(self):
        """ Test if the target class without a singleton attribute but using a decorator with primitive parameters. """
        try:
            @singleton(10)
            class SuperDummyClass(TestDecoratorCommonSingletonClass.DummyTest):
                def __init__(self, init_number):
                    super(self.__class__, self).__init__()
                    self.number = init_number
            self.assertTrue(True, 'Singleton Class: Passed the initialization as expected.')
        except SingletonInitializationException:
            self.assertTrue(False, 'Singleton Class: Failed the initialization with known exception.')
        
        # Test for the type.
        self.assertIsInstance(SuperDummyClass.instance(), SuperDummyClass)
        # Test if it is working. (case #1)
        SuperDummyClass.instance().take_action()
        self.assertEqual(SuperDummyClass.instance().get_number(), 11)
        # Test if it is working. (case #n)
        SuperDummyClass.instance().take_action()
        self.assertEqual(SuperDummyClass.instance().get_number(), 12)
    
    def test_positive_for_normal_singleton_with_parameters(self):
        """ Positive test for @singleton with parameters provided for the constructor """
        try:
            class SampleDependencyInjection(object): pass
            sample_di = SampleDependencyInjection()
            @singleton(sample_di)
            class SuperDummyClass(TestDecoratorCommonSingletonClass.DummyTest):
                def __init__(self, dependency_injection):
                    super(self.__class__, self).__init__()
                    self.dependency_injection = dependency_injection
            self.assertTrue(True, 'Singleton Class: Passed the initialization as expected.')
        except SingletonInitializationException:
            self.assertTrue(False, 'Singleton Class: Failed the initialization with known exception.')
        
        # Test for the type.
        self.assertIsInstance(SuperDummyClass.instance(), SuperDummyClass)
        # Test if it is working. (case #1)
        SuperDummyClass.instance().take_action()
        self.assertEqual(SuperDummyClass.instance().get_number(), 1)
        # Test if it is working. (case #n)
        SuperDummyClass.instance().take_action()
        self.assertEqual(SuperDummyClass.instance().get_number(), 2)
        # Test if the dependency injection is working.
        self.assertIsInstance(SuperDummyClass.instance().dependency_injection, SampleDependencyInjection)
    
    def test_negative_for_normal_singleton_with_class_reference(self):
        """ Negative test for @singleton with class_reference provided for the constructor """
        
        # Note that this test case shows the limitation of the decorator which
        # can't take a class reference as a parameter. Strongly recommend to
        # use @singleton_with as it is more powerful.
        
        try:
            class SampleDependencyInjection(object): pass
            @singleton(SampleDependencyInjection)
            class SuperDummyClass(TestDecoratorCommonSingletonClass.DummyTest):
                def __init__(self, dependency_injection):
                    super(self.__class__, self).__init__()
                    self.dependency_injection = dependency_injection
            self.assertTrue(False, 'Singleton Class: Passed the initialization as expected.')
        except SingletonInitializationException:
            self.assertTrue(False, 'Singleton Class: Failed the initialization with known-yet-unexpected exception.')
        except TypeError:
            self.assertTrue(True, 'Singleton Class: Failed the initialization with expected exception.')
    
    def test_positive_for_singleton_with(self):
        """ Positive test for @singleton_with(*args, **kwargs) """
        
        # Note that this test case shows the limitation of the decorator which
        # can't take a class reference as a parameter. Strongly recommend to
        # use @singleton_with as it is more powerful.
        
        try:
            class SampleDependencyInjection(object): pass
            @singleton_with(SampleDependencyInjection)
            class SuperDummyClass(TestDecoratorCommonSingletonClass.DummyTest):
                def __init__(self, dependency_injection):
                    super(self.__class__, self).__init__()
                    self.dependency_injection = dependency_injection()
            self.assertTrue(True, 'Singleton Class: Passed the initialization as expected.')
        except SingletonInitializationException:
            self.assertTrue(False, 'Singleton Class: Failed the initialization with known exception.')
        
        # Test for the type.
        self.assertIsInstance(SuperDummyClass.instance(), SuperDummyClass)
        # Test if it is working. (case #1)
        SuperDummyClass.instance().take_action()
        self.assertEqual(SuperDummyClass.instance().get_number(), 1)
        # Test if it is working. (case #n)
        SuperDummyClass.instance().take_action()
        self.assertEqual(SuperDummyClass.instance().get_number(), 2)
        # Test if the dependency injection is working.
        self.assertIsInstance(SuperDummyClass.instance().dependency_injection, SampleDependencyInjection)
    
    def test_negative_with_existed_singleton_instance(self):
        """ Test if the target class is with null singleton attribute. """
        try:
            @singleton
            class SuperDummyClass(TestDecoratorCommonSingletonClass.DummyTest):
                _singleton_instance = None
                def __init__(self):
                    # Use `self.__class__` to call the parent class' constructor.
                    super(self.__class__, self).__init__()
            self.assertTrue(False, 'Singleton Class: Passed the initialization unexpectedly.')
        except SingletonInitializationException:
            self.assertTrue(True, 'Singleton Class: Failed the initialization with expected exception.')
    
    def test_negative_with_unexpected_instance_attr(self):
        """ Test if the target class has already had an attribute `_singleton_instance` but it is not compatible. """
        try:
            @singleton
            class SuperDummyClass(TestDecoratorCommonSingletonClass.DummyTest):
                _singleton_instance = {}
                def __init__(self):
                    # Use `self.__class__` to call the parent class' constructor.
                    super(self.__class__, self).__init__()
            self.assertTrue(False, 'Singleton Class: Passed the initialization unexpectedly.')
        except SingletonInitializationException:
            self.assertTrue(True, 'Singleton Class: Failed the initialization with expected exception.')

if __name__ == '__main__':
    unittest.main()