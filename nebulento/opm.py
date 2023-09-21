from ovos_plugin_manager.templates.pipeline import IntentPipelinePlugin, IntentMatch
from ovos_utils import classproperty

from nebulento import IntentContainer, MatchStrategy


def _munge(name, skill_id):
    return f"{name}:{skill_id}"


def _unmunge(munged):
    return munged.split(":", 2)


class NebulentoPipelinePlugin(IntentPipelinePlugin):

    def __init__(self, bus, config=None):
        super().__init__(bus, config)
        fuzzy_strategy = self.config.get("fuzzy_strategy", "ratio")
        if fuzzy_strategy == "ratio":
            fuzzy_strategy = MatchStrategy.RATIO
        elif fuzzy_strategy == "token_set_ratio":
            fuzzy_strategy = MatchStrategy.TOKEN_SET_RATIO
        elif fuzzy_strategy == "token_sort_ratio":
            fuzzy_strategy = MatchStrategy.TOKEN_SORT_RATIO
        elif fuzzy_strategy == "partial_token_set_ratio":
            fuzzy_strategy = MatchStrategy.PARTIAL_TOKEN_SET_RATIO
        elif fuzzy_strategy == "partial_token_sort_ratio":
            fuzzy_strategy = MatchStrategy.PARTIAL_TOKEN_SORT_RATIO
        else:
            fuzzy_strategy = MatchStrategy.SIMPLE_RATIO
        self.fuzzy_strategy = fuzzy_strategy
        self.engines = {}  # lang: IntentContainer

    # plugin api
    @classproperty
    def matcher_id(self):
        return "nebulento"

    def match(self, utterances, lang, message):
        for utt in utterances:
            return self.calc_intent(utt, lang=lang)

    def train(self):
        # no training step needed
        return True

    # implementation
    def _get_engine(self, lang=None):
        lang = lang or self.lang
        if lang not in self.engines:
            self.engines[lang] = IntentContainer(fuzzy_strategy=self.fuzzy_strategy)
        return self.engines[lang]

    def detach_intent(self, skill_id, intent_name):
        munged = _munge(intent_name, skill_id)
        for lang in self.engines:
            if munged in self.engines[lang].registered_intents:
                self.engines[lang].registered_intents.remove(munged)
        super().detach_intent(intent_name)

    def register_entity(self, skill_id, entity_name, samples=None, lang=None):
        lang = lang or self.lang
        super().register_entity(skill_id, entity_name, samples, lang)
        engine = self._get_engine(lang)
        munged = _munge(entity_name, skill_id)
        engine.add_entity(munged, samples)

    def register_intent(self, skill_id, intent_name, samples=None, lang=None):
        lang = lang or self.lang
        super().register_intent(skill_id, intent_name, samples, lang)
        engine = self._get_engine(lang)
        munged = _munge(intent_name, skill_id)
        engine.add_intent(munged, samples)

    # matching
    def calc_intent(self, utterance, min_conf=0.6, lang=None):
        lang = lang or self.lang
        engine = self._get_engine(lang)
        intent = engine.calc_intent(utterance)

        if intent["conf"] < min_conf:
            return None

        # HACK - nebulento returns a list, api expects single entry
        intent["entities"] = {k: v[0] for k, v in intent["entities"].items() if v}

        intent_type, skill_id = _unmunge(intent["name"])
        return IntentMatch(intent_service=self.matcher_id,
                           intent_type=intent_type,
                           intent_data=intent["entities"],
                           confidence=intent["conf"],
                           utterance=utterance,
                           skill_id=skill_id)
