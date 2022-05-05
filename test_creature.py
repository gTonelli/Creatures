import unittest
import creature


class TestCreature(unittest.TestCase):

    def testCreatureExists(self):
        self.assertIsNotNone(creature.Creature)

    def testCreatureGetFlatLinks(self):
        c = creature.Creature(gene_count=4)
        links = c.get_flat_links()
        self.assertEqual(len(links), 4)

    def testExpandedLinks(self):
        c = creature.Creature(gene_count=4)
        links = c.get_flat_links()
        expanded_links = c.get_expanded_links()
        self.assertGreaterEqual(len(expanded_links), len(links))


unittest.main()
