#!/usr/bin/env python3

# Project: VUT FIT ATA Project - Řízení vozíku v robotické továrně
# Author: Dominik Harmim <xharmi00@stud.fit.vutbr.cz>
# Year: 2021
# Description: Cart controller implementation testing.

import unittest

from cart import Cart, CargoReq, Status as CartStatus, CartError
from cartctl import CartCtl, Status as CartCtlStatus, LongPrioRequestError
from jarvisenv import Jarvis


class TestCartRequests(unittest.TestCase):
    """ A test suite for the cart controller testing. """

    def setUp(self) -> None:
        """ The set-up phase for each test method in the class. """
        super().setUp()
        Jarvis.reset_scheduler()

    @staticmethod
    def log(msg: str) -> None:
        """ Simple logging. """
        print(f'  {msg}')

    @staticmethod
    def add_load(cart_ctl: CartCtl, cargo_req: CargoReq) -> None:
        """ A callback for schedulled load. """
        TestCartRequests.log(f'{Jarvis.time()}: Requesting {cargo_req} at {cargo_req.src}')
        cart_ctl.request(cargo_req)

    @staticmethod
    def log_on_move(cart: Cart) -> None:
        """ On-move logging. """
        TestCartRequests.log(f'{Jarvis.time()}: Cart is moving {cart.pos} -> {cart.data}')
        TestCartRequests.log(f'{cart}')

    @staticmethod
    def log_on_load(cart: Cart, cargo_req: CargoReq) -> None:
        """ On-load logging. """
        TestCartRequests.log(f'{Jarvis.time()}: Cart at {cart.pos}: loading: {cargo_req}')
        TestCartRequests.log(f'{cart}')

    @staticmethod
    def log_on_unload(cart: Cart, cargo_req: CargoReq) -> None:
        """ On-unload logging. """
        TestCartRequests.log(f'{Jarvis.time()}: Cart at {cart.pos}: unloading: {cargo_req}')
        TestCartRequests.log(f'{cart}')

    def test_happy(self) -> None:
        """ A happy-path test. """

        def on_move(cart: Cart) -> None:
            """ A callback for schedulled move. """
            self.log_on_move(cart)
            self.assertEqual(CartStatus.Moving, cart.status)

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            cargo_req.context = 'loaded'
            self.assertEqual(CartStatus.Idle, cart.status)
            self.assertIn(cargo_req, cart.slots)
            if cargo_req.content == 'helmet':
                self.assertEqual('A', cart.pos)
            elif cargo_req.content == 'heart':
                self.assertEqual('C', cart.pos)
            elif cargo_req.content == 'braceletR':
                self.assertEqual('D', cart.pos)
            elif cargo_req.content == 'braceletL':
                self.assertEqual('D', cart.pos)

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            self.assertEqual(CartStatus.Idle, cart.status)
            self.assertNotIn(cargo_req, cart.slots)
            if cargo_req.content == 'helmet':
                self.assertEqual('B', cart.pos)
            elif cargo_req.content == 'heart':
                self.assertEqual('A', cart.pos)
            elif cargo_req.content == 'braceletR':
                self.assertEqual('A', cart.pos)
            elif cargo_req.content == 'braceletL':
                self.assertEqual('C', cart.pos)

        # setup cart
        cart = Cart(4, 150, 0)
        cart.onmove = on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        helmet = CargoReq('A', 'B', 20, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('C', 'A', 40, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        bracelet_r = CargoReq('D', 'A', 40, 'braceletR')
        bracelet_r.onload = on_load
        bracelet_r.onunload = on_unload

        bracelet_l = CargoReq('D', 'C', 40, 'braceletL')
        bracelet_l.onload = on_load
        bracelet_l.onunload = on_unload

        # setup plan
        Jarvis.plan(10, self.add_load, (cart_ctl, helmet))
        Jarvis.plan(45, self.add_load, (cart_ctl, heart))
        Jarvis.plan(40, self.add_load, (cart_ctl, bracelet_r))
        Jarvis.plan(25, self.add_load, (cart_ctl, bracelet_l))

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertTrue(cart.empty())
        self.assertEqual('unloaded', helmet.context)
        self.assertEqual('unloaded', heart.context)
        self.assertEqual('unloaded', bracelet_r.context)
        self.assertEqual('unloaded', bracelet_l.context)
        self.assertEqual(cart.pos, 'C')
        self.assertEqual(CartStatus.Idle, cart.status)

    def test_no_request(self) -> None:
        """
        A test with no requests made.
        Covers: CEG.1
        """

        def on_move(cart: Cart) -> None:
            """ A callback for schedulled move. """
            self.log_on_move(cart)
            self.fail('The cart should not be moving.')

        # setup cart
        cart = Cart(1, 500, 0)
        cart.onmove = on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertEqual(CartCtlStatus.Idle, cart_ctl.status)
        self.assertTrue(cart.empty())
        self.assertIn(None, cart.slots)
        self.assertGreater(cart.load_capacity, 0)
        self.assertEqual(cart.pos, 'A')

    def test_process_basic_request(self) -> None:
        """
        A test that processes a single basic request.
        Covers: CEG.2
        """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertEqual('helmet', cargo_req.content)
            self.assertIn(cargo_req, cart.slots)
            self.assertLess(Jarvis.time(), 10 + 60)
            self.assertFalse(cargo_req.prio)
            self.assertEqual('A', cart.pos)
            cargo_req.context = 'loaded'

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            self.assertEqual('helmet', cargo_req.content)
            self.assertNotIn(cargo_req, cart.slots)
            self.assertEqual('B', cart.pos)

        def check_cart_ctl_status(cart_ctl: CartCtl) -> None:
            """ Checkes the cart controller status after loading. """
            self.assertEqual(CartCtlStatus.Normal, cart_ctl.status)

        # setup cart
        cart = Cart(3, 150, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        helmet = CargoReq('A', 'B', 50, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        # setup plan
        Jarvis.plan(10, self.add_load, (cart_ctl, helmet))
        Jarvis.plan(20, check_cart_ctl_status, (cart_ctl,))

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertEqual(CartCtlStatus.Idle, cart_ctl.status)
        self.assertTrue(cart.empty())
        self.assertEqual('unloaded', helmet.context)
        self.assertEqual(cart.pos, 'B')

    def test_process_prio_request(self) -> None:
        """
        A test that processes a prioritised request.
        Covers: CEG.3
        """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertIn(cargo_req, cart.slots)
            self.assertTrue(cargo_req.prio)
            cargo_req.context = 'loaded'
            if cargo_req.content == 'helmet':
                self.assertGreaterEqual(Jarvis.time(), 1 + 60)
                self.assertLess(Jarvis.time(), 1 + 60 + 60)
                self.assertEqual('D', cart.pos)
            elif cargo_req.content == 'heart':
                self.assertGreaterEqual(Jarvis.time(), 70 + 60)
                self.assertLess(Jarvis.time(), 70 + 60 + 60)
                self.assertEqual('B', cart.pos)

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            self.assertNotIn(cargo_req, cart.slots)
            if cargo_req.content == 'helmet':
                self.assertEqual('C', cart.pos)
            elif cargo_req.content == 'heart':
                self.assertEqual('D', cart.pos)

        def check_cart_ctl_status(cart_ctl: CartCtl) -> None:
            """ Checkes the cart controller status after loading. """
            self.assertEqual(CartCtlStatus.UnloadOnly, cart_ctl.status)

        # setup cart
        cart = Cart(1, 150, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        helmet = CargoReq('D', 'C', 50, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('B', 'D', 50, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        # setup plan
        Jarvis.plan(1, self.add_load, (cart_ctl, helmet))
        Jarvis.plan(65, check_cart_ctl_status, (cart_ctl,))
        Jarvis.plan(70, self.add_load, (cart_ctl, heart))
        Jarvis.plan(170, check_cart_ctl_status, (cart_ctl,))

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertEqual(CartCtlStatus.Idle, cart_ctl.status)
        self.assertTrue(cart.empty())
        self.assertEqual('unloaded', helmet.context)
        self.assertEqual('unloaded', heart.context)
        self.assertEqual(cart.pos, 'D')

    def test_no_free_slots(self) -> None:
        """
        A test that throws an exception due to no free cart's slots.
        Covers: CEG.4
        """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertEqual('baz', cargo_req.content)
            self.fail('baz should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('baz', cargo_req.content)
            self.fail('baz should not be unloaded.')

        def check_cart_ctl_status(cart_ctl: CartCtl) -> None:
            """ Checkes the cart controller status before an exception is thrown. """
            self.assertEqual('baz', cart_ctl.requests[0].content)
            self.assertTrue(cart_ctl.requests[0].prio)

        # setup cart
        cart = Cart(1, 150, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('D', 'B', 50, 'foo')
        foo.onload = self.log_on_load
        foo.onunload = self.log_on_unload

        bar = CargoReq('B', 'C', 50, 'bar')
        bar.onload = self.log_on_load
        bar.onunload = self.log_on_unload

        baz = CargoReq('A', 'D', 50, 'baz')
        baz.onload = on_load
        baz.onunload = on_unload

        # setup plan
        Jarvis.plan(0, self.add_load, (cart_ctl, foo))
        Jarvis.plan(24, self.add_load, (cart_ctl, bar))
        Jarvis.plan(25, self.add_load, (cart_ctl, baz))
        Jarvis.plan(125, check_cart_ctl_status, (cart_ctl,))

        # exercise + verify indirect output
        self.assertRaises(LongPrioRequestError, Jarvis.run)

        self.log(f'{cart}')

    def test_no_capacity(self) -> None:
        """
        A test that throws an exception due to no cart's capacity.
        Covers: CEG.5
        """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertEqual('baz', cargo_req.content)
            self.fail('baz should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('baz', cargo_req.content)
            self.fail('baz should not be unloaded.')

        def check_cart_ctl_status(cart_ctl: CartCtl) -> None:
            """ Checkes the cart controller status before an exception is thrown. """
            self.assertEqual('baz', cart_ctl.requests[0].content)
            self.assertTrue(cart_ctl.requests[0].prio)

        # setup cart
        cart = Cart(2, 150, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('D', 'B', 100, 'foo')
        foo.onload = self.log_on_load
        foo.onunload = self.log_on_unload

        bar = CargoReq('B', 'C', 100, 'bar')
        bar.onload = self.log_on_load
        bar.onunload = self.log_on_unload

        baz = CargoReq('A', 'D', 140, 'baz')
        baz.onload = on_load
        baz.onunload = on_unload

        # setup plan
        Jarvis.plan(0, self.add_load, (cart_ctl, foo))
        Jarvis.plan(24, self.add_load, (cart_ctl, bar))
        Jarvis.plan(25, self.add_load, (cart_ctl, baz))
        Jarvis.plan(125, check_cart_ctl_status, (cart_ctl,))

        # exercise + verify indirect output
        self.assertRaises(LongPrioRequestError, Jarvis.run)

        self.log(f'{cart}')

    def test_combine_1(self) -> None:
        """ Covers: Combine.1 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.fail('foo should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.fail('foo should not be unloaded.')

        # setup cart
        cart = Cart(1, 150, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('A', 'A', 200, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        # setup plan
        Jarvis.plan(0, self.add_load, (cart_ctl, foo))

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertTrue(cart.empty())
        self.assertEqual(cart.pos, 'A')

    def test_combine_2(self) -> None:
        """ Covers: Combine.2 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            if cargo_req.content == 'foo':
                self.fail('foo should not be loaded.')
            elif cargo_req.content == 'bar':
                self.fail('bar should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            if cargo_req.content == 'foo':
                self.fail('foo should not be unloaded.')
            elif cargo_req.content == 'bar':
                self.fail('bar should not be unloaded.')

        # setup cart
        cart = Cart(2, 50, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('A', 'A', 10, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        bar = CargoReq('A', 'A', 20, 'bar')
        bar.onload = on_load
        bar.onunload = on_unload

        # setup plan
        Jarvis.plan(20, self.add_load, (cart_ctl, foo))
        Jarvis.plan(20, self.add_load, (cart_ctl, bar))

        # exercise + verify indirect output
        self.assertRaises(CartError, Jarvis.run)

        self.log(f'{cart}')

    def test_combine_3(self) -> None:
        """ Covers: Combine.3 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.assertIn(cargo_req, cart.slots)
            self.assertEqual('A', cart.pos)
            cargo_req.context = 'loaded'

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            self.assertNotIn(cargo_req, cart.slots)
            self.assertEqual('A', cart.pos)

        # setup cart
        cart = Cart(4, 50, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('A', 'A', 10, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        # setup plan
        Jarvis.plan(0, self.add_load, (cart_ctl, foo))

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertTrue(cart.empty())
        self.assertEqual('unloaded', foo.context)
        self.assertEqual(cart.pos, 'A')

    def test_combine_4(self) -> None:
        """ Covers: Combine.4 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            if cargo_req.content == 'foo':
                self.fail('foo should not be loaded.')
            elif cargo_req.content == 'bar':
                self.fail('bar should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            if cargo_req.content == 'foo':
                self.fail('foo should not be unloaded.')
            elif cargo_req.content == 'bar':
                self.fail('bar should not be unloaded.')

        # setup cart
        cart = Cart(1, 500, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('A', 'B', 10, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        bar = CargoReq('A', 'B', 2000, 'bar')
        bar.onload = on_load
        bar.onunload = on_unload

        # setup plan
        Jarvis.plan(0, self.add_load, (cart_ctl, foo))
        Jarvis.plan(0, self.add_load, (cart_ctl, bar))

        # exercise + verify indirect output
        self.assertRaises(CartError, Jarvis.run)

        self.log(f'{cart}')

    def test_combine_5(self) -> None:
        """ Covers: Combine.5 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.fail('foo should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.fail('foo should not be unloaded.')

        # setup cart
        cart = Cart(2, 150, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('A', 'B', 200, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        # setup plan
        Jarvis.plan(50, self.add_load, (cart_ctl, foo))

        # exercise + verify indirect output
        Jarvis.run()

        self.log(f'{cart}')

    def test_combine_6(self) -> None:
        """ Covers: Combine.6 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            if cargo_req.content == 'foo':
                self.fail('foo should not be loaded.')
            elif cargo_req.content == 'bar':
                self.fail('bar should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            if cargo_req.content == 'foo':
                self.fail('foo should not be unloaded.')
            elif cargo_req.content == 'bar':
                self.fail('bar should not be unloaded.')

        # setup cart
        cart = Cart(3, 50, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('A', 'B', 100, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        bar = CargoReq('B', 'C', 10, 'bar')
        bar.onload = on_load
        bar.onunload = on_unload

        # setup plan
        Jarvis.plan(50, self.add_load, (cart_ctl, foo))
        Jarvis.plan(50, self.add_load, (cart_ctl, bar))

        # exercise + verify indirect output
        self.assertRaises(CartError, Jarvis.run)

        self.log(f'{cart}')

    def test_combine_7(self) -> None:
        """ Covers: Combine.7 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            if cargo_req.content == 'foo':
                self.fail('foo should not be loaded.')
            elif cargo_req.content == 'bar':
                self.fail('bar should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            if cargo_req.content == 'foo':
                self.fail('foo should not be unloaded.')
            elif cargo_req.content == 'bar':
                self.fail('bar should not be unloaded.')

        # setup cart
        cart = Cart(1, 150, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('A', 'C', 100, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        bar = CargoReq('A', 'C', 50, 'bar')
        bar.onload = on_load
        bar.onunload = on_unload

        # setup plan
        Jarvis.plan(50, self.add_load, (cart_ctl, foo))
        Jarvis.plan(50, self.add_load, (cart_ctl, bar))

        # exercise + verify indirect output
        self.assertRaises(CartError, Jarvis.run)

        self.log(f'{cart}')

    def test_combine_8(self) -> None:
        """ Covers: Combine.8 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.fail('foo should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.fail('foo should not be unloaded.')

        # setup cart
        cart = Cart(2, 500, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('A', 'C', 600, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        # setup plan
        Jarvis.plan(0, self.add_load, (cart_ctl, foo))

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertTrue(cart.empty())
        self.assertEqual(cart.pos, 'A')

    def test_combine_9(self) -> None:
        """ Covers: Combine.9 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.fail('foo should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.fail('foo should not be unloaded.')

        # setup cart
        cart = Cart(4, 50, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('A', 'C', 120, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        # setup plan
        Jarvis.plan(0, self.add_load, (cart_ctl, foo))

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertTrue(cart.empty())
        self.assertEqual(cart.pos, 'A')

    def test_combine_10(self) -> None:
        """ Covers: Combine.10 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.fail('foo should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.fail('foo should not be unloaded.')

        # setup cart
        cart = Cart(3, 150, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('A', 'A', 200, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        # setup plan
        Jarvis.plan(0, self.add_load, (cart_ctl, foo))

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertTrue(cart.empty())
        self.assertEqual(cart.pos, 'A')

    def test_combine_11(self) -> None:
        """ Covers: Combine.11 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.assertIn(cargo_req, cart.slots)
            self.assertEqual('D', cart.pos)
            cargo_req.context = 'loaded'

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            self.assertNotIn(cargo_req, cart.slots)
            self.assertEqual('D', cart.pos)

        # setup cart
        cart = Cart(1, 500, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('D', 'D', 300, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        # setup plan
        Jarvis.plan(100, self.add_load, (cart_ctl, foo))

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertTrue(cart.empty())
        self.assertEqual('unloaded', foo.context)
        self.assertEqual(cart.pos, 'D')

    def test_combine_12(self) -> None:
        """ Covers: Combine.12 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            if cargo_req.content == 'foo':
                self.fail('foo should not be loaded.')
            elif cargo_req.content == 'bar':
                self.fail('bar should not be loaded.')

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            if cargo_req.content == 'foo':
                self.fail('foo should not be loaded.')
            elif cargo_req.content == 'bar':
                self.fail('bar should not be loaded.')

        # setup cart
        cart = Cart(4, 50, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('A', 'A', 200, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        bar = CargoReq('A', 'A', 200, 'bar')
        bar.onload = on_load
        bar.onunload = on_unload

        # setup plan
        Jarvis.plan(0, self.add_load, (cart_ctl, foo))
        Jarvis.plan(20, self.add_load, (cart_ctl, bar))

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertTrue(cart.empty())
        self.assertEqual(cart.pos, 'A')

    def test_combine_13(self) -> None:
        """ Covers: Combine.13 """

        def on_load(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled loading. """
            self.log_on_load(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.assertIn(cargo_req, cart.slots)
            self.assertEqual('D', cart.pos)
            cargo_req.context = 'loaded'

        def on_unload(cart: Cart, cargo_req: CargoReq) -> None:
            """ A callback for schedulled unloading. """
            self.log_on_unload(cart, cargo_req)
            self.assertEqual('foo', cargo_req.content)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            self.assertNotIn(cargo_req, cart.slots)
            self.assertEqual('A', cart.pos)

        # setup cart
        cart = Cart(1, 150, 0)
        cart.onmove = self.log_on_move

        # setup cart controller
        cart_ctl = CartCtl(cart, Jarvis)

        # setup cargo to move
        foo = CargoReq('D', 'A', 150, 'foo')
        foo.onload = on_load
        foo.onunload = on_unload

        # setup plan
        Jarvis.plan(0, self.add_load, (cart_ctl, foo))

        # exercise + verify indirect output
        Jarvis.run()

        # verify direct output
        self.log(f'{cart}')
        self.assertTrue(cart.empty())
        self.assertEqual('unloaded', foo.context)
        self.assertEqual(cart.pos, 'A')


if __name__ == '__main__':
    unittest.main()
