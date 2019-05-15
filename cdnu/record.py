import json
from typing import List, NamedTuple


class Record(NamedTuple):
    """A record representing an individual genome."""

    seq_url: str
    index_url: str
    sample_name: str
    population: str

    def to_dict(self) -> dict:
        return {
            'seqUrl': self.seq_url,
            'indexUrl': self.index_url,
            'sampleName': self.sample_name,
            'population': self.population
        }

    def from_dict(record_dict):
        seq_url = record_dict['seqUrl']
        index_url = record_dict['indexUrl']
        sample_name = record_dict['sampleName']
        population = record_dict['population']
        return Record(seq_url=seq_url, index_url=index_url,
                      sample_name=sample_name, population=population)


def load_index(index_file_path: str) -> List[Record]:
    """Load a record index and preserve ordering."""
    with open(index_file_path, encoding='utf-8', newline='\n') as fp:
        index_list = json.load(fp)

    assert isinstance(index_list, list)
    return [Record.from_dict(r) for r in index_list]


def save_index(index_file_path: str, records: List[Record]):
    """Store a record index and preserve ordering."""
    index_list = [r.to_dict() for r in records]

    with open(index_file_path, 'w', encoding='utf-8', newline='\n') as fp:
        json.dump(index_list, fp)
