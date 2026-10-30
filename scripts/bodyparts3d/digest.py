# Picture jobs for the digestive chapter, read by jobs.py: the digestive organs drawn see-through inside the trunk, with one
# organ in red. BodyParts3D has the gut as separate models (oesophagus, stomach, duodenum, jejunum, ileum, colon as one
# piece, rectum, appendix), the liver, gallbladder, pancreas and its duct, the spleen and the teeth.
TRUNK_BONES = ids(r'\brib$', r'costal cartilage', r'^manubrium$', r'^body of sternum$', r'^xiphoid', r'thoracic vertebra', r'lumbar vertebra', r'^sacrum$', r'hip bone', r'right femur$', r'left femur$')
GUT = ids(r'^esophagus$', r'^stomach$', r'^duodenum$', r'^jejunum$', r'^ileum$', r'^colon', r'^rectum$', r'^appendix$', r'anal sphincter')
GLANDS = ids(r'^liver$', r'^gallbladder$', r'^pancreas', r'pancreatic duct', r'^spleen$')
ABD = ids(r'^stomach$', r'^liver$', r'^colon', r'^rectum$', r'^ileum$')
def dg(name, *pats, view='front', focus=None, xray=True, bones=True, extra=(), hide=(), pad=1.1, w=800, h=800, **kw):
    hi = ids(*pats)
    only = [i for i in (TRUNK_BONES if bones else []) + GUT + GLANDS + ids(*extra) if i not in set(hide)]
    J[name] = {'view': view, 'hi': hi, 'focus': focus or ABD + ids(r'^esophagus$'), 'only': only, 'xray': xray, 'w': w, 'h': h, 'pad': pad, **kw}
dg('d-tract', r'^esophagus$', r'^stomach$', r'^duodenum$', r'^jejunum$', r'^ileum$', r'^colon', r'^rectum$', r'^appendix$', r'anal sphincter')
dg('d-esophagus', r'^esophagus$')
dg('d-stomach', r'^stomach$')
dg('d-duodenum', r'^duodenum$', focus=ids(r'^duodenum$', r'^pancreas', r'^stomach$'), pad=1.6)
dg('d-jejunum', r'^jejunum$')
dg('d-ileum', r'^ileum$')
dg('d-small-intestine', r'^duodenum$', r'^jejunum$', r'^ileum$')
dg('d-colon', r'^colon')
dg('d-rectum', r'^rectum$', r'anal sphincter', focus=ids(r'^rectum$', r'anal sphincter', r'^colon'), pad=1.6)
dg('d-appendix', r'^appendix$', focus=ids(r'^appendix$', r'^ileum$', r'^colon'), pad=1.7)
dg('d-liver', r'^liver$')
dg('d-gallbladder', r'^gallbladder$', focus=ids(r'^liver$', r'^gallbladder$', r'^duodenum$'), pad=1.6)
dg('d-pancreas', r'^pancreas', focus=ids(r'^pancreas', r'^duodenum$', r'^spleen$'), pad=1.6)
dg('d-pancreatic-duct', r'pancreatic duct', focus=ids(r'^pancreas', r'^duodenum$'), pad=1.8)
dg('d-spleen', r'^spleen$', focus=ABD + ids(r'^spleen$'))
TEETH = ids(r'tooth')
J['d-teeth'] = {'view': 'front', 'hi': TEETH, 'focus': SKULL, 'only': SKULL + NECK, 'xray': False, 'w': 800, 'h': 700, 'pad': 1.1}
J['d-incisors'] = {**J['d-teeth'], 'hi': ids(r'incisor tooth')}
J['d-canines'] = {**J['d-teeth'], 'hi': ids(r'canine tooth')}
J['d-premolars'] = {**J['d-teeth'], 'hi': ids(r'premolar tooth')}
J['d-molars'] = {**J['d-teeth'], 'hi': ids(r'secondary molar tooth')}
