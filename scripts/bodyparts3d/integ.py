# Picture jobs for the integumentary chapter, read by jobs.py: the skin, head hair and eyebrows, drawn see-through over the
# skeleton or the head, with one part in red. BodyParts3D has the skin as one surface, so the layers, glands and nails are
# text questions.
SKIN = ids(r'^skin$')
HAIR = ids(r'set of head hairs', r'set of eyebrows')
def ig(name, *pats, view='front', focus=None, only=None, xray=True, pad=1.1, w=800, h=800, **kw):
    J[name] = {'view': view, 'hi': ids(*pats), 'focus': focus or SKIN, 'only': only if only is not None else SKIN + HAIR + ALL, 'xray': xray, 'w': w, 'h': h, 'pad': pad, **kw}
ig('i-skin', r'^skin$', only=SKIN + ALL)
ig('i-skin-back', r'^skin$', only=SKIN + ALL, view='back')
ig('i-hair', r'set of head hairs', focus=ids(r'set of head hairs', r'set of eyebrows'), only=SKIN + HAIR + ids(r'^(?!.*(rib|vertebra)).*skull|mandible|frontal|parietal'), pad=1.4, view='left')
ig('i-eyebrows', r'set of eyebrows', focus=ids(r'set of eyebrows', r'set of head hairs'), only=SKIN + HAIR, pad=1.5)
