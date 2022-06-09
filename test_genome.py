import unittest
import genome
import numpy as np
from xml.dom.minidom import getDOMImplementation
import os

class GenomeTest(unittest.TestCase):

    def testClassExists(self):
        self.assertIsNotNone(genome.Genome)

    def testRandomeGene(self):
        self.assertIsNotNone(genome.Genome.get_random_gene)

    def testRandomeGeneNotNone(self):
        self.assertIsNotNone(genome.Genome.get_random_gene(5))

    def testRandomeGeneHasValues(self):
        gene = genome.Genome.get_random_gene(5)
        self.assertIsNotNone(gene[0])

    def testRandomeGeneLength(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(len(gene), 20)

    def testRandGeneIsNumpyArray(self):
        gene = genome.Genome.get_random_gene(20)
        self.assertEqual(type(gene), np.ndarray)

    def testRandomGenomeExists(self):
        data = genome.Genome.get_random_genome(20, 5)
        self.assertIsNotNone(data)

    def testGeneSpecExists(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec)

    def testGeneSpecHasLinkLength(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length'])

    def testGeneSpecHasIndex(self):
        spec = genome.Genome.get_gene_spec()
        self.assertIsNotNone(spec['link-length']["index"])

    def testGeneSpecScale(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(20)
        self.assertGreater(gene[spec['link-length']["index"]], 0)

    def testGeneToGeneDict(self):
        spec = genome.Genome.get_gene_spec()
        gene = genome.Genome.get_random_gene(len(spec))
        gene_dict = genome.Genome.get_gene_dict(gene, spec)
        self.assertIn('link-recurrence', gene_dict)

    def testGenomeToDict(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        self.assertEqual(len(genome_dicts), 3)

    def testFlatLinks(self):
        links = [
            genome.URDFLink(name="A", parent_name=None, recur=1),
            genome.URDFLink(name="A", parent_name="A", recur=1),
            genome.URDFLink(name="A", parent_name="B", recur=2),
            genome.URDFLink(name="A", parent_name="C", recur=1)
        ]
        self.assertIsNotNone(links)

    def testExpandLinks(self):
        links = [
            genome.URDFLink(name="A", parent_name=None, recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=2)
        ]
        expanded_links = [links[0]]
        genome.Genome.expandLinks(
            links[0], links[0].name, links, expanded_links)
        self.assertEqual(len(expanded_links), 3)

    def testExpandLinks2(self):
        links = [
            genome.URDFLink(name="A", parent_name=None, recur=1),
            genome.URDFLink(name="B", parent_name="A", recur=1),
            genome.URDFLink(name="C", parent_name="B", recur=2),
            genome.URDFLink(name="D", parent_name="C", recur=1)
        ]
        expanded_links = [links[0]]
        genome.Genome.expandLinks(
            links[0], links[0].name, links, expanded_links)
        self.assertEqual(len(expanded_links), 6)

    def testGetLinks(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        links = genome.Genome.genome_to_links(genome_dicts)
        self.assertEqual(len(links), 3)

    def testGetLinksUniqueNames(self):
        spec = genome.Genome.get_gene_spec()
        dna = genome.Genome.get_random_genome(len(spec), 3)
        genome_dicts = genome.Genome.get_genome_dicts(dna, spec)
        links = genome.Genome.genome_to_links(genome_dicts)

        for l in links:
            names = [link.name for link in links if link.name == l.name]
            self.assertEqual(len(names), 1)

    def testLinkToXML(self):
        link = genome.URDFLink(name="A", parent_name="None", recur=1)
        dom_impl = getDOMImplementation()
        xmlDOM = dom_impl.createDocument(None, "robot", None)
        xml_string = link.to_link_element(xmlDOM)
        self.assertIsNotNone(xml_string)

    def testCrossover(self):
        g1 = np.array([[1,2,3], [4,5,6], [7,8,9]])
        g2 = np.array([[10,11,12], [13,14,15], [16,17,18]])
        g3 = genome.Genome.crossover(g1, g2)
        self.assertEqual(len(g3), len(g1))

    def testPoint(self):
        g1 = np.array([[1.,2.,3.], [4.,5.,6.], [7.,8.,9.]])
        genome.Genome.point_mutate(g1, rate=0.5, amount=0.25)

    def testShrink(self):
        g1 = np.array([[1.,2.,3.], [4.,5.,6.], [7.,8.,9.]])
        g2 = genome.Genome.shrink_mutate(g1, rate=1)
        self.assertNotEqual(len(g1), len(g2))

    def testGrow(self):
        g1 = np.array([[1.,2.,3.], [4.,5.,6.], [7.,8.,9.]])
        g2 = genome.Genome.grow_mutate(g1, rate=1)
        self.assertGreater(len(g2), len(g1))

    def testToCSV(self):
        g1 = [[1,2,3]]
        genome.Genome.dna_to_csv(g1, 'test/test.csv')
        self.assertTrue(os.path.exists('test/test.csv'))

    def testToCSVContent(self):
        g1 = [[1,2,3]]
        genome.Genome.dna_to_csv(g1, 'test/test.csv')
        expect = "1,2,3,\n"
        with open('test/test.csv') as f:
            csv_string = f.read()

        self.assertEqual(csv_string, expect)

    def testToCSVContent2(self):
        g1 = [[1,2,3], [4,5,6]]
        genome.Genome.dna_to_csv(g1, 'test/test.csv')
        expect = "1,2,3,\n4,5,6,\n"
        with open('test/test.csv') as f:
            csv_string = f.read()

        self.assertEqual(csv_string, expect)

    def testFromCSV(self):
        g1 = [[1,2,3]]
        genome.Genome.dna_to_csv(g1, 'test/test.csv')
        g2 = genome.Genome.dna_from_csv('test/test.csv')
        self.assertTrue(np.array_equal(g1, g2))

    def testFromCSV2(self):
        g1 = [[1,2,3], [4,5,6]]
        genome.Genome.dna_to_csv(g1, 'test/test.csv')
        g2 = genome.Genome.dna_from_csv('test/test.csv')
        self.assertTrue(np.array_equal(g1, g2))


unittest.main()
