import unittest
import genome
import numpy as np
from xml.dom.minidom import getDOMImplementation


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

    def testLinkToXML(self):
        link = genome.URDFLink(name="A", parent_name="None", recur=1)
        dom_impl = getDOMImplementation()
        xmlDOM = dom_impl.createDocument(None, "robot", None)
        xml_string = link.to_link_xml(xmlDOM)
        print(xml_string)
        self.assertIsNotNone(xml_string)


unittest.main()
