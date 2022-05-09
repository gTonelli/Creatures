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
                Genome.expandLinks(c, unique_name, flat_links, expanded_links)

    @staticmethod
    def genome_to_links(genome_dicts):
        links = []
        link_index = 0
        parent_names = [str(link_index)]

        for genome_dict in genome_dicts:
            link_name = str(link_index)
            parent_index = genome_dict["joint-parent"] * len(parent_names)
            recur = int(round(genome_dict["link-recurrence"]))
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

    def to_link_xml(self, xmlDOM):
        link_tag = xmlDOM.createElement("link")
        link_tag.setAttribute("name", self.name)
        visual_tag = xmlDOM.createElement('visual')
        geometry_tag = xmlDOM.createElement("geometry")
        cylinder_tag = xmlDOM.createElement("cylinder")
        cylinder_tag.setAttribute("length", str(self.link_length))
        cylinder_tag.setAttribute("radius", str(self.link_radius))
        geometry_tag.appendChild(cylinder_tag)
        visual_tag.appendChild(geometry_tag)
        link_tag.appendChild(visual_tag)

        return link_tag.toprettyxml()
