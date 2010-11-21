#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <tornado bdd sample>
# Copyright (C) <2010>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
import tornado.ioloop
import tornado.httpserver

from threading import Thread
from lettuce import before, after, world
from sample import application
from selenium import get_driver, FIREFOX

class Server(Thread):
    def __init__(self, http):
        self.http = http
        Thread.__init__(self)

    def run(self):
        self.http.listen(8888)
        tornado.ioloop.IOLoop.instance().start()

@before.all
def run_server():
    world._server_main = tornado.httpserver.HTTPServer(application)
    server = Server(world._server_main)
    server.start()

@before.all
def setup_browser():
    world.browser = get_driver(FIREFOX)

@after.all
def kill_server(total):
    world._server_main.stop()
    tornado.ioloop.IOLoop.instance().stop()

@after.all
def teardown_browser(total):
    world.browser.quit()
