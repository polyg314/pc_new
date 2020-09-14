import os
import glob
import pymongo
# when code is exported, import becomes relative
try:
    from pubchem.pubchem_parser import load_data as parser_func
except ImportError:
    from .pubchem_parser import load_data as parser_func


# from parser import load_data
from hub.dataload.uploader import BaseDrugUploader
from biothings.hub.dataload.uploader import ParallelizedSourceUploader
import biothings.hub.dataload.storage as storage

class PubChemUploader(BaseDrugUploader,ParallelizedSourceUploader):

    name = "pubchem"
    storage_class = storage.IgnoreDuplicatedStorage

    __metadata__ = { "src_meta" : {
        "url": "https://pubchem.ncbi.nlm.nih.gov/",
        "license_url" : "https://www.ncbi.nlm.nih.gov/home/about/policies/",
        "license_url_short" : "http://bit.ly/2AqoLOc",
        "license": "public domain"
        }
    }

    COMPOUND_PATTERN = "Compound*.xml.gz"

    def jobs(self):
        # this will generate arguments for self.load.data() method, allowing parallelization
        xmlgz_files = glob.glob(os.path.join(self.data_folder,self.__class__.COMPOUND_PATTERN))
        return [(f,) for f in xmlgz_files]

    def load_data(self,input_file):
        self.logger.info("Load data from file '%s'" % input_file)
        return parser_func(input_file)

    @classmethod
    def get_mapping(klass):
        return {
                "pubchem" : {
                    "properties" : {
                        "inchi_key" : {
                            "normalizer": "keyword_lowercase_normalizer",
                            "type": "keyword",
                            },
                        "undefined_atom_stereocenter_count" : {
                            "type":"integer"
                            },
                        "formal_charge" : {
                            "type":"integer"
                            },
                        "isotope_atom_count" : {
                            "type":"integer"
                            },
                        "defined_atom_stereocenter_count" : {
                            "type":"integer"
                            },
                        "molecular_weight" : {
                            "type":"float"
                            },
                        "monoisotopic_weight" : {
                            "type":"float"
                            },
                        "tautomers_count" : {
                            "type":"integer"
                            },
                        "rotatable_bond_count" : {
                            "type":"integer"
                            },
                        "exact_mass" : {
                            "type":"float"
                            },
                        "chiral_bond_count" : {
                            "type":"integer"
                            },
                        "smiles" : {
                            "properties" : {
                                "isomeric" : {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    },
                                "canonical" : {
                                    "normalizer": "keyword_lowercase_normalizer",
                                    "type": "keyword",
                                    }
                                }
                            },
                        "hydrogen_bond_acceptor_count" : {
                            "type":"integer"
                            },
                        "hydrogen_bond_donor_count" : {
                                "type":"integer"
                                },
                        "inchi" : {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword",
                                },
                        "undefined_bond_stereocenter_count" : {
                                "type":"integer"
                                },
                        "defined_bond_stereocenter_count" : {
                                "type":"integer"
                                },
                        "xlogp" : {
                                "type":"float"
                                },
                        "chiral_atom_count" : {
                                "type":"integer"
                                },
                        "cid" : {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword",
                                'copy_to': ['all'],
                                },
                        "topological_polar_surface_area" : {
                                "type":"float"
                                },
                        "iupac" : {
                                "properties" : {
                                    "traditional" : {
                                        "type":"text"
                                        }
                                    }
                                },
                        "complexity" : {
                                "type":"float"
                                },
                        "heavy_atom_count" : {
                                "type":"integer"
                                },
                        "molecular_formula" : {
                                "normalizer": "keyword_lowercase_normalizer",
                                "type": "keyword",
                                },
                        "covalently-bonded_unit_count" : {
                                "type":"integer"
                                }
                        }
                }
            }

