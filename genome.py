from audioop import cross
import numpy as np
import copy
import math


class Genome():
    @staticmethod
    def get_random_gene(length):
        gene = np.array([np.random.random() for i in range(length)])
        return gene

    @staticmethod
    def get_random_genome(gene_length, gene_count):
        genome = [Genome.get_random_gene(gene_length)
                  for i in range(gene_count)]
        return genome

    @staticmethod
    def get_gene_spec():
        gene_spec = {
            "link-shape": {"scale": 1},
            "link-length": {"scale": 1},
            "link-radius": {"scale": 1},
            "link-recurrence": {"scale": 4},
            "link-mass": {"scale": 1},

            "joint-type": {"scale": 1},
            "joint-parent": {"scale": 1},

            # 3 options [1, 0, 0] or [0, 1, 0] or [0, 0, 1]
            "joint-axis-xyz": {"scale": 1},
            "joint-origin-rpy-1": {"scale": np.pi * 2},
            "joint-origin-rpy-2": {"scale": np.pi * 2},
            "joint-origin-rpy-3": {"scale": np.pi * 2},
            "joint-origin-xyz-1": {"scale": 1},
            "joint-origin-xyz-2": {"scale": 1},
            "joint-origin-xyz-3": {"scale": 1},

            "control-waveform": {"scale": 1},
            "control-amp": {"scale": 0.25},
            "control-freq": {"scale": 1}
        }

        index = 0

        for key in gene_spec.keys():
            gene_spec[key]["index"] = index
            index = index + 1

        return gene_spec

    @staticmethod
    def get_gene_dict(gene, spec):
        gene_dict = {}

        for key in spec.keys():
            gene_dict[key] = spec[key]["scale"] * gene[spec[key]["index"]]
        return gene_dict

    @staticmethod
    def get_genome_dicts(dna, spec):
        genome_dicts = [Genome.get_gene_dict(gene, spec) for gene in dna]
        return genome_dicts

    @staticmethod
    def expandLinks(parent_link, unique_parent_name, flat_links, expanded_links):
        children = [l for l in flat_links if l.parent_name == parent_link.name]
        sibling_index = 1
        for c in children:
            for r in range(c.recur):
                sibling_index = sibling_index + 1
                c_copy = copy.copy(c)
                c_copy.parent_name = unique_parent_name
                unique_name = c_copy.name + str(len(expanded_links))
                c_copy.name = unique_name
                c_copy.sibling_index = sibling_index
                expanded_links.append(c_copy)
                assert c.parent_name != c.name, "Genome::expandLinks: link joined to itself: " + \
                    c.name + " joins " + c.parent_name
                Genome.expandLinks(c, unique_name, flat_links, expanded_links)

    @staticmethod
    def genome_to_links(genome_dicts):
        links = []
        link_index = 0
        parent_names = [str(link_index)]
        for genome_dict in genome_dicts:
            link_name = str(link_index)
            parent_index = genome_dict["joint-parent"] * len(parent_names)
            recur = int(math.ceil(genome_dict["link-recurrence"]))
            parent_name = parent_names[int(parent_index)]
            link = URDFLink(
                name=link_name, parent_name=parent_name, recur=recur+1,
                link_length=genome_dict["link-length"],
                link_radius=genome_dict["link-radius"],
                link_mass=genome_dict["link-mass"],
                joint_type=genome_dict["joint-type"],
                joint_parent=genome_dict["joint-parent"],
                joint_axis_xyz=genome_dict["joint-axis-xyz"],
                joint_origin_rpy_1=genome_dict["joint-origin-rpy-1"],
                joint_origin_rpy_2=genome_dict["joint-origin-rpy-2"],
                joint_origin_rpy_3=genome_dict["joint-origin-rpy-3"],
                joint_origin_xyz_1=genome_dict["joint-origin-xyz-1"],
                joint_origin_xyz_2=genome_dict["joint-origin-xyz-2"],
                joint_origin_xyz_3=genome_dict["joint-origin-xyz-3"],
                control_waveform=genome_dict["control-waveform"],
                control_amp=genome_dict["control-amp"],
                control_freq=genome_dict["control-freq"])
            links.append(link)
            if link_index != 0:
                parent_names.append(link_name)
            link_index = link_index + 1

        links[0].parent_name = "None"
        return links
    
    @staticmethod
    def crossover(g1, g2):
        xo = np.random.randint(len(g1)) # TODO: Change this to generate a number so that the if statement below is needless
        # xo = np.random.randint(1, len(g1))
        if xo > len(g2):
            xo = len(g2) - 1

        g3 = np.concatenate((g1[0:xo], g2[xo:]))
        return g3

    @staticmethod
    def point_mutate(genes, rate, amount):
        for gene in genes:
            if np.random.rand() < rate:
                index = np.random.randint(len(gene))
                r = (np.random.rand() - 0.5) * amount
                gene[index] = gene[index] + r

    @staticmethod
    def shrink_mutate(genes, rate):
        if np.random.rand() < rate:
            index = np.random.randint(len(genes))
            genes = np.delete(genes, index, 0)
        return genes

    @staticmethod
    def grow_mutate(genes, rate):
        if np.random.rand() < rate:
            gene = Genome.get_random_gene(len(genes[0]))
            genes = np.append(genes, [gene], axis=0)
        return genes



class URDFLink:
    def __init__(self, name, parent_name, recur,
                 link_length=0.1,
                 link_radius=0.1,
                 link_mass=0.1,
                 joint_type=0.1,
                 joint_parent=0.1,
                 joint_axis_xyz=0.1,
                 joint_origin_rpy_1=0.1,
                 joint_origin_rpy_2=0.1,
                 joint_origin_rpy_3=0.1,
                 joint_origin_xyz_1=0.1,
                 joint_origin_xyz_2=0.1,
                 joint_origin_xyz_3=0.1,
                 control_waveform=0.1,
                 control_amp=0.1,
                 control_freq=0.1):
        self.name = name
        self.parent_name = parent_name
        self.recur = recur
        self.link_length = link_length
        self.link_radius = link_radius
        self.link_mass = link_mass
        self.joint_type = joint_type
        self.joint_parent = joint_parent
        self.joint_axis_xyz = joint_axis_xyz
        self.joint_origin_rpy_1 = joint_origin_rpy_1
        self.joint_origin_rpy_2 = joint_origin_rpy_2
        self.joint_origin_rpy_3 = joint_origin_rpy_3
        self.joint_origin_xyz_1 = joint_origin_xyz_1
        self.joint_origin_xyz_2 = joint_origin_xyz_2
        self.joint_origin_xyz_3 = joint_origin_xyz_3
        self.control_waveform = control_waveform
        self.control_amp = control_amp
        self.control_freq = control_freq
        self.sibling_index = 1

    def to_link_element(self, xmlDOM):
        link_tag = xmlDOM.createElement("link")
        link_tag.setAttribute("name", self.name)
        visual_tag = xmlDOM.createElement('visual')
        geometry_tag = xmlDOM.createElement("geometry")
        cylinder_tag = xmlDOM.createElement("cylinder")
        cylinder_tag.setAttribute("length", str(self.link_length))
        cylinder_tag.setAttribute("radius", str(self.link_radius))

        geometry_tag.appendChild(cylinder_tag)
        visual_tag.appendChild(geometry_tag)

        collision_tag = xmlDOM.createElement("collision")
        collision_geometry_tag = xmlDOM.createElement("geometry")
        collision_cylinder_tag = xmlDOM.createElement("cylinder")
        collision_cylinder_tag.setAttribute("length", str(self.link_length))
        collision_cylinder_tag.setAttribute("radius", str(self.link_radius))

        collision_geometry_tag.appendChild(collision_cylinder_tag)
        collision_tag.appendChild(collision_geometry_tag)

        inertial_tag = xmlDOM.createElement("inertial")
        mass_tag = xmlDOM.createElement("mass")

        mass = np.pi * (self.link_radius * self.link_radius) * self.link_length
        mass_tag.setAttribute("value", str(mass))
        inertia_tag = xmlDOM.createElement("inertia")

        inertia_tag.setAttribute("ixx", "0.03")
        inertia_tag.setAttribute("iyy", "0.03")
        inertia_tag.setAttribute("izz", "0.03")
        inertia_tag.setAttribute("ixy", "0")
        inertia_tag.setAttribute("ixz", "0")
        inertia_tag.setAttribute("iyx", "0")
        inertial_tag.appendChild(mass_tag)
        inertial_tag.appendChild(inertia_tag)

        link_tag.appendChild(visual_tag)
        link_tag.appendChild(collision_tag)
        link_tag.appendChild(inertial_tag)

        return link_tag

    def to_joint_element(self, xmlDOM):

        joint_tag = xmlDOM.createElement("joint")
        joint_tag.setAttribute("name", self.name + "_to_" + self.parent_name)
        if self.joint_type >= 0.5:
            joint_tag.setAttribute("type", "revolute")
        else:
            joint_tag.setAttribute("type", "revolute")

        parent_tag = xmlDOM.createElement("parent")
        parent_tag.setAttribute("link", self.parent_name)
        child_tag = xmlDOM.createElement("child")
        child_tag.setAttribute("link", self.name)
        axis_tag = xmlDOM.createElement("axis")
        if self.joint_axis_xyz <= 0.33:
            axis_tag.setAttribute("xyz", "1 0 0")
        if self.joint_axis_xyz > 0.33 and self.joint_axis_xyz <= 0.66:
            axis_tag.setAttribute("xyz", "0 1 0")
        if self.joint_axis_xyz > 0.66:
            axis_tag.setAttribute("xyz", "0 0 1")

        limit_tag = xmlDOM.createElement("limit")
        # effort upper lower velocity
        limit_tag.setAttribute("effort", "1")
        limit_tag.setAttribute("upper", "-3.1415")
        limit_tag.setAttribute("lower", "3.1415")
        limit_tag.setAttribute("velocity", "1")

        origin_tag = xmlDOM.createElement("origin")

        rpy3 = self.joint_origin_rpy_3 * self.sibling_index
        rpy = str(self.joint_origin_rpy_1) + " " + str(self.joint_origin_rpy_2) + \
            " " + str(rpy3)
        origin_tag.setAttribute("rpy", rpy)

        xyz = str(self.joint_origin_xyz_1) + " " + \
            str(self.joint_origin_xyz_2) + " " + str(self.joint_origin_xyz_3)
        origin_tag.setAttribute("xyz", xyz)

        joint_tag.appendChild(parent_tag)
        joint_tag.appendChild(child_tag)
        joint_tag.appendChild(axis_tag)
        joint_tag.appendChild(limit_tag)
        joint_tag.appendChild(origin_tag)
        return joint_tag
