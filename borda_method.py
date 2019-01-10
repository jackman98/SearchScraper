from constants import SEARCH_ENGINE_EVALUATION

class MetasearchResultsAggregator:

    def __init__(self, engines_links):
        
        self._engines_links = engines_links
                
        # Will use as P - set of all unique alternative
        self.all_unique_links = set()

        for _, engine in enumerate(self._engines_links):
            engine_links = self._engines_links[engine]
            self.all_unique_links.update(engine_links)
	        
        self.range_sequence_length = len(self.all_unique_links)

    def get_ranked_link_list(self):
        # TODO: will implemented later
        return []