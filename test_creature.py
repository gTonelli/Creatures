import unittest
import creature
import pybullet as p
import numpy as np


class TestCreature(unittest.TestCase):

    def testCreatureExists(self):
        self.assertIsNotNone(creature.Creature)

    def testCreatureGetFlatLinks(self):
        c = creature.Creature(gene_count=4)
        links = c.get_flat_links()
        self.assertEqual(len(links), 4)

    def testExpandedLinks(self):
        for i in range(1000):
            c = creature.Creature(gene_count=4)
            links = c.get_flat_links()
            expanded_links = c.get_expanded_links()
            self.assertGreaterEqual(len(expanded_links), len(links))

    def testToXMLNotNone(self):
        c = creature.Creature(gene_count=2)
        xml_str = c.to_xml()
        self.assertIsNotNone(xml_str)

    def testLoadXML(self):
        c = creature.Creature(gene_count=3)
        xml_str = c.to_xml()
        with open('test.urdf', 'w') as f:
            f.write(xml_str)
        p.connect(p.DIRECT)
        cid = p.loadURDF('test.urdf')
        self.assertIsNotNone(cid)

    def testMotor(self):
        m = creature.Motor(0.1, 0.5, 0.5)
        self.assertIsNotNone(m)

    def testMotorValuePulse(self):
        m = creature.Motor(0.1, 0.5, 0.5)
        self.assertEqual(m.get_output(), 1)

    def testMotorValueSine(self):
        m = creature.Motor(0.6, 0.5, 0.5)
        k = 2
        for i in range(k):
            m.get_output()
        self.assertGreater(m.get_output(), 0)

    def testXreatureMotors(self):
        c = creature.Creature(gene_count=4)
        ls = c.get_expanded_links()
        ms = c.get_motors()
        self.assertEqual(len(ls) - 1, len(ms))


unittest.main()
