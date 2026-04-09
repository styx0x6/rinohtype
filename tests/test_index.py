from rinoh.index import IndexSee, IndexSeeAlso, IndexTarget, IndexTerm


class DummyDocument(object):
    def __init__(self):
        self.ids_by_element = {}
        self.index_entries = {}

    def register_element(self, _element):
        return None

class DummyFlowableTarget(object):
    def __init__(self, document):
        self.document = document


def test_index_see_construction():
    assert tuple(IndexSee('term', 'reference')) == ('term', 'reference')
    assert tuple(IndexSeeAlso('term', 'reference')) == ('term', 'reference')

def test_target_index_entries():
    document = DummyDocument()
    flowable_target = DummyFlowableTarget(document)
    index_target = IndexTarget([
        IndexTerm('single_term1', 'single_term2', 'single_term3'),
        IndexTerm('single_term4'),
        IndexTerm('pair_term1', 'pair_term2'),
        IndexTerm('pair_term2', 'pair_term1'),
        IndexTerm('module', 'search' + ' ' + 'path'),
        IndexTerm('search', 'path' + ', ' + 'module'),
        IndexTerm('path', 'module' + ' ' + 'search'),
        IndexSee('term', 'synonym_term'),
        IndexSeeAlso('term2', 'synonym_term2'),
    ])
    index_target.id = 'index-target'

    index_target.prepare(flowable_target)

    assert document.index_entries == {
        'single_term1': ('single_term1', {None: [(IndexTerm('single_term1'), index_target)]}),
        'single_term2': ('single_term2', {None: [(IndexTerm('single_term2'), index_target)]}),
        'single_term3': ('single_term3', {None: [(IndexTerm('single_term3'), index_target)]}),
        'single_term4': ('single_term4', {None: [(IndexTerm('single_term4'), index_target)]}),
        'pair_term1': ('pair_term1', {None: [(IndexTerm('pair_term1', 'pair_term2'), index_target)]}),
        'pair_term2': ('pair_term2', {None: [(IndexTerm('pair_term2', 'pair_term1'), index_target)]}),
        'module': ('module', {None: [(IndexTerm('module', 'search' + ' ' + 'path'), index_target)]}),
        'search': ('search', {None: [(IndexTerm('search', 'path' + ', ' + 'module'), index_target)]}),
        'path': ('path', {None: [(IndexTerm('path', 'module' + ' ' + 'search'), index_target)]}),
        'term': ('term', {'_index_see': ['synonym_term']}),
        'term2': ('term2', {'_index_seealso': ['synonym_term2']}),
    }
