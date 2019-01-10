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
        self.engines_ranked_dict = dict()
        for _, engine in enumerate(self._engines_links):
            engine_links = self._engines_links[engine]
            self.unique_link_counts[engine] = len(engine_links)

            engine_ranked_list = dict(zip(self._engines_links[engine], range(len(engine_links))))
            self.engines_ranked_dict[engine] = engine_ranked_list

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
                self.engines_ranked_dict[engine][link] = new_rank

        print(self.engines_ranked_dict)


    def get_ranked_link_list(self):
        # TODO: will implemented later
        
        self.engine_vi = dict()
        self.engine_oi = dict()
        for _, engine in enumerate(self._engines_links):
            if self.all_links_count != 0:
                self.engine_vi[engine] = self.unique_link_counts[engine] / self.all_links_count
            else:
                self.engine_vi[engine] = 0

            if self.range_sequence_length != 0:
                self.engine_oi[engine] = self.unique_link_counts[engine] / self.range_sequence_length
            else:
                self.engine_oi[engine] = 0

        print('Vi', self.engine_vi)
        print('Oi', self.engine_oi)

        finding_counter = 0
        for _, link in enumerate(self.all_unique_links):
            for _, engine in enumerate(self._engines_links):
                if link in self._engines_links[engine]:
                    finding_counter += 1
        
        print(f"Sum Hj = {finding_counter}")

        p = finding_counter / (self._searchers_count * self.range_sequence_length)
        
        x1, x2 = 1 - p, p

        print(f"x1 = {x1}, x2 = {x2}")

        self.engine_wi_abnormal = dict()
        sum_wi = 0
        for _, engine in enumerate(self._engines_links):
            ei = SEARCH_ENGINE_EVALUATION[engine]
            oi = self.engine_oi[engine]
            vi = self.engine_vi[engine]
            self.engine_wi_abnormal[engine] = ei * (x1 * oi + x2 * vi)
            sum_wi += self.engine_wi_abnormal[engine]

        self.engine_wi = dict()
        for _, engine in enumerate(self._engines_links):
            self.engine_wi[engine] = self.engine_wi_abnormal[engine] / sum_wi
        
        print(f"Wi = {self.engine_wi}")

        self.ranked_link_list = []
        for _, link in enumerate(self.all_unique_links):
            summary_rank = 0
            for _, engine in enumerate(self._engines_links):
                if link in self.engines_ranked_dict[engine]:
                    summary_rank += self.engines_ranked_dict[engine][link]
            
            self.ranked_link_list.append(dict({"link": link, "rank": summary_rank}))

        return self.ranked_link_list
