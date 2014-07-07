#!/usr/bin/env python
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, test_view,\
    test_depends, install_module, suite as tryton_suite
from trytond.transaction import Transaction


class TestCase(unittest.TestCase):
    'Test module'

    def setUp(self):
        install_module('party_relationship_position')
        self.party = POOL.get('party.party')
        self.relation_type = POOL.get('party.relation.type')
        self.position = POOL.get('party.relation.position')
        self.relation = POOL.get('party.relation')
        self.relation_all = POOL.get('party.relation.all')

    def test0005views(self):
        'Test views'
        test_view('party_relationship_position')

    def test0006depends(self):
        'Test depends'
        test_depends()

    def test0010reverse_relationship(self):
        'Test reverse relationship'
        with Transaction().start(DB_NAME, USER, context=CONTEXT):
            position, = self.position.create([{
                        'name': 'Director',
                        }])
            employee_of, = self.relation_type.create([{
                        'name': 'Employee of',
                        }])
            works_for, = self.relation_type.create([{
                        'name': 'Works for',
                        'reverse': employee_of.id,
                        }])
            self.relation_type.write([employee_of], {
                        'reverse': works_for.id,
                        })

            company, employee = self.party.create([{
                        'name': 'Company',
                        }, {
                        'name': 'Employee',
                        }])

            self.relation.create([{
                        'from_': company.id,
                        'to': employee.id,
                        'type': employee_of.id,
                        'position': position,
                        }])
            company_relation, = company.relations
            employee_relation, = employee.relations
            self.assertEqual(company_relation.type, employee_of)
            self.assertEqual(company_relation.to, employee)
            self.assertEqual(company_relation.position, position)
            self.assertEqual(employee_relation.type, works_for)
            self.assertEqual(employee_relation.to, company)
            self.assertEqual(employee_relation.position, position)


def suite():
    suite = tryton_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    return suite
