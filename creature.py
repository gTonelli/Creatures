import genome


class Creature:
    def __init__(self, gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)
        self.flat_links = None

    def get_flat_links(self):
        genome_dicts = genome.Genome.get_genome_dicts(self.dna, self.spec)
        if(self.flat_links != None):
            return self.flat_links

        self.flat_links = genome.Genome.genome_to_links(genome_dicts)
        return self.flat_links

    def get_expanded_links(self):
        self.get_flat_links()
        expanded_links = []
        genome.Genome.expandLinks(
            self.flat_links[0], self.flat_links[0].name, self.flat_links, expanded_links)
        self.expanded_links = expanded_links
        return self.expanded_links
