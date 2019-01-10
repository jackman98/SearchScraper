from constants import SEARCH_ENGINE_EVALUATION

class MetasearchResultsAggregator:

    def __init__(self, engines_links):
        
        self._engines_links = engines_links
        self._searchers_count = len(engines_links)
        print (f"Searchers count = {self._searchers_count}")
                
        # Will use as P - set of all unique alternative
        self.all_unique_links = set()
        self.all_links_count = 0

        # TODO confirm mi 
        self.unique_link_counts = dict()
        engines_ranked_dict = dict()
        for _, engine in enumerate(self._engines_links):
            engine_links = self._engines_links[engine]
            self.unique_link_counts[engine] = len(engine_links)

            engine_ranked_list = dict(zip(self._engines_links[engine], range(len(engine_links))))
            engines_ranked_dict[engine] = engine_ranked_list

            self.all_unique_links.update(engine_links)
            self.all_links_count += len(engine_links)

        # We have set of all unique links
        # Next confirm length of ranging sequence
        self.range_sequence_length = len(self.all_unique_links)

        print('Mi', self.unique_link_counts)

        # Add all other alternatives
        print('UNIFIED_UNION')
        for _, engine in enumerate(self._engines_links):
            new_rank = self.unique_link_counts[engine]

            engine_links_set = set(self._engines_links[engine])
            difference_links = self.all_unique_links - engine_links_set
            for link in difference_links:
                engines_ranked_dict[engine][link] = new_rank

        print(engines_ranked_dict)


    def get_ranked_link_list(self):
        # TODO: will implemented later
        return []