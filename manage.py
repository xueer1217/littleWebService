#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Application is the glue between one or more service definitions, interface and protocol choices.
from spyne import Application
# @rpc decorator exposes methods as remote procedure calls
# and declares the data types it accepts and returns
from spyne import rpc
# spyne.service.ServiceBase is the base class for all service definitions.
from spyne import ServiceBase
# The names of the needed types for implementing this service should be self-explanatory.
from spyne import Iterable, Integer, Unicode

from spyne.protocol.soap import Soap11
# Our server is going to use HTTP as transport, It’s going to wrap the Application instance.
from spyne.server.wsgi import WsgiApplication


# step1: Defining a Spyne Service
class StudentInfoService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Iterable(Unicode))
    def get_student_info(self, name, password):
        """Docstrings for service methods appear as documentation in the wsdl.
        <b>What fun!</b>
        @param name: student name
        @param password: student password to verify
        @return  When returning an iterable, you can use any type of python iterable. Here, we chose to use generators.
        """

        verify_info_dict = {"stu1": "pwd1", "stu2": "pwd2"}

        student_info_dict = {'stu1': 'age : 22 ; major : computer science ;',
                             'stu2': 'age : 23 ; major : electronic commerce;'}
        res = verify_info_dict.get(name, '')

        if res == password:
            yield student_info_dict.get(name, 'no student info in database')
        else:
            yield "name or password wrong"

    @rpc(Unicode, Unicode, _returns=Iterable(Unicode))
    def verify_student_info(self, name, password):
        """Docstrings for service methods appear as documentation in the wsdl.
        <b>What fun!</b>
        @param name: student name
        @param password: student password to verify
        @return  When returning an iterable, you can use any type of python iterable. Here, we chose to use generators.
        """

        verify_info_dict = {"stu1": "pwd1", "stu2": "pwd2"}

        res = verify_info_dict.get(name, '')

        if res == password:
            yield bool(1)
        else:
            yield bool(0)


# step2: Glue the service definition, input and output protocols
soap_app = Application([StudentInfoService], 'studentInfo.soap',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

# step3: Wrap the Spyne application with its wsgi wrapper
wsgi_app = WsgiApplication(soap_app)

if __name__ == '__main__':
    # main()
    import logging
    from wsgiref.simple_server import make_server

    # configure the python logger to show debugging output
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('studentInfo.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    # step4:Deploying the service using Soap via Wsgi
    # register the WSGI application as the handler to the wsgi server, and run the http server
    server = make_server('127.0.0.1', 8000, wsgi_app)
    server.serve_forever()
