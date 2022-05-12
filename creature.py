import genome
from xml.dom.minidom import getDOMImplementation
from enum import Enum
import numpy as np


class MotorType(Enum):
    PULSE = 1
    SINE = 2


class Motor:
    def __init__(self, control_waveform, control_amplitude, control_frequency):
        if control_waveform <= 0.5:
            self.motor_type = MotorType.PULSE
        else:
            self.motor_type = MotorType.SINE
        self.amp = control_amplitude
        self.freq = control_frequency
        self.phase = 0

    def get_output(self):
        self.phase = (self.phase + self.freq) % (np.pi * 2)

        if self.motor_type == MotorType.PULSE:
            if self.phase < np.pi:
                output = 1
            else:
                output = -1

        if self.motor_type == MotorType.SINE:
            output = np.sin(self.phase)

        return output


class Creature:
    def __init__(self, gene_count):
        self.spec = genome.Genome.get_gene_spec()
        self.dna = genome.Genome.get_random_genome(len(self.spec), gene_count)
        self.flat_links = None
        self.expanded_links = None
        self.motors = None

    def get_flat_links(self):
        genome_dicts = genome.Genome.get_genome_dicts(self.dna, self.spec)
        if(self.flat_links != None):
            return self.flat_links

        self.flat_links = genome.Genome.genome_to_links(genome_dicts)
        return self.flat_links

    def get_expanded_links(self):
        self.get_flat_links()

        if self.expanded_links is not None:
            return self.expanded_links

        expanded_links = [self.flat_links[0]]
        genome.Genome.expandLinks(
            self.flat_links[0], self.flat_links[0].name, self.flat_links, expanded_links)
        self.expanded_links = expanded_links
        return self.expanded_links

    def to_xml(self):
        self.get_expanded_links()
        dom_implementation = getDOMImplementation()
        adom = dom_implementation.createDocument(None, "start", None)
        robot_tag = adom.createElement("robot")
        for link in self.expanded_links:
            robot_tag.appendChild(link.to_link_element(adom))
        first = True
        for link in self.expanded_links:
            if first:  # skip the parent node
                first = False
                continue
            robot_tag.appendChild(link.to_joint_element(adom))
        robot_tag.setAttribute("name", "joe")  # Robots name!
        return '<?xml version="1.0"?>' + robot_tag.toprettyxml()

    def get_motors(self):
        assert(self.expanded_links != None)
        if self.motors == None:
            motors = []
            for i in range(1, len(self.expanded_links)):
                l = self.expanded_links[i]
                m = Motor(l.control_waveform, l.control_amp, l.control_freq)
                motors.append(m)
            self.motors = motors
        return self.motors
