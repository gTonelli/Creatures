import unittest
import creature
import pybullet as p


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
        c = creature.Creature(gene_count=2)
        xml_str = c.to_xml()
        with open('test.urdf', 'w') as f:
            f.write(xml_str)
        p.connect(p.DIRECT)

        # p.connect(p.GUI)
        # p.setPhysicsEngineParameter(enableFileCaching=0)
        # p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        # plane_shape = p.createCollisionShape(p.GEOM_PLANE)
        # floor = p.createMultiBody(plane_shape, plane_shape)
        # p.setGravity(0, 0, -10)

        cid = p.loadURDF('test.urdf')
        self.assertIsNotNone(cid)


unittest.main()
