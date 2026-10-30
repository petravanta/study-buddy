# Picture jobs for the anatomy chapters: which BodyParts3D parts to colour, and from where to look.
import json, os, re, sys
P = [(l.split('\t') + ['bone'])[:3] for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'parts.tsv')).read().strip().split('\n')]
def ids(*pats):
    out = []
    for pat in pats:
        r = re.compile(pat)
        m = [i for i, n, _ in P if r.search(n)]
        if not m: sys.exit('no part matches ' + pat)
        out += m
    return out
ALL = [i for i, _, k in P if k in ('bone', 'cartilage')]  # the skeleton
MUSCLES = [i for i, _, k in P if k in ('muscle', 'tendon')]
BRAIN = [i for i, _, k in P if k == 'brain']
ARTERIES = [i for i, _, k in P if k == 'artery']
VEINS = [i for i, _, k in P if k == 'vein']
HEART = [i for i, _, k in P if k == 'heart']
LUNGS = [i for i, _, k in P if k == 'lung']
AIRWAYS = [i for i, _, k in P if k == 'airway']
ORGANS = [i for i, _, k in P if k == 'organ']
SKULL = ids(r'^(frontal|occipital|sphenoid) bone$', r'temporal bone', r'parietal bone', r'^ethmoid$', r'^mandible$', r'zygomatic bone', r'lacrimal', r'nasal bone', r'maxilla', r'palatine', r'concha', r'^vomer$', r'tooth')
NECK = ids(r'^atlas$', r'^axis$', r'(third|fourth|fifth) cervical', r'^hyoid bone$')
COLUMN = ids(r'vertebra$', r'^atlas$', r'^axis$', r'^sacrum$', r'intervertebral')
THORAX = ids(r'\brib$', r'costal cartilage', r'^manubrium$', r'^body of sternum$', r'^xiphoid')
R_HAND = ids(r'right (scaphoid|lunate|triquetral|pisiform|trapezium|trapezoid|capitate|hamate)$', r'right \w+ metacarpal', r'phalanx of right (thumb|\w+ finger)')
R_FOOT = ids(r'right (talus|calcaneus|cuboid bone)$', r'navicular bone of right', r'right \w+ cuneiform', r'right \w+ metatarsal', r'phalanx of right (big|second|third|fourth|little) toe', r'sesamoid bone of right')
BODY = dict(view='front', focus=ALL, w=560, h=1000, pad=1.04)
J = {}
def body(name, *pats, **kw): J[name] = {**BODY, 'hi': ids(*pats), **kw}
def skull(name, *pats, view='left', **kw): J[name] = {'view': view, 'hi': ids(*pats), 'focus': SKULL, 'only': SKULL + NECK, 'w': 800, 'h': 700, **kw}
# Whole skeleton
J['skeleton'] = dict(BODY)
J['skeleton-axial'] = {**BODY, 'hi': ids(r'vertebra$', r'^atlas$', r'^axis$', r'^sacrum$', r'\brib$', r'^manubrium$', r'^body of sternum$', r'^xiphoid', r'^hyoid bone$') + SKULL}
J['skeleton-appendicular'] = {**BODY, 'hi': ids(r'clavicle', r'scapula$', r'humerus', r'radius', r'ulna$', r'hip bone', r'femur', r'patella', r'tibia$', r'fibula$') + ids(r'(left|right) (scaphoid|lunate|triquetral|pisiform|trapezium|trapezoid|capitate|hamate)$', r'metacarpal', r'phalanx', r'(talus|calcaneus|cuboid bone)$', r'navicular bone of', r'cuneiform', r'metatarsal', r'sesamoid')}
# Skull
skull('frontal', r'^frontal bone$', view=[.5, -1, .1])
skull('parietal', r'parietal bone')
skull('temporal', r'temporal bone')
skull('occipital', r'^occipital bone$', view=[.6, 1, .1])
skull('sphenoid', r'^sphenoid bone$')
FACE = ids(r'maxilla', r'nasal bone', r'^ethmoid$', r'zygomatic bone')
skull('ethmoid', r'^ethmoid$', view=[.6, -1, .2], xray=True, focus=FACE)
skull('mandible', r'^mandible$')
skull('maxilla', r'maxilla', view='front')
skull('zygomatic', r'zygomatic bone')
skull('nasal', r'nasal bone', view=[.5, -1, .1])
skull('lacrimal', r'lacrimal', view=[.7, -1, .1])
skull('vomer', r'^vomer$', view=[.6, -1, .1], xray=True, focus=FACE)
skull('palatine', r'palatine', view='bottom', hide=ids(r'^mandible$', r'lower .*tooth') + NECK)
skull('concha', r'concha', view='front', xray=True)
J['hyoid'] = {'view': [1, -.6, .1], 'hi': ids(r'^hyoid bone$'), 'focus': SKULL + NECK, 'only': SKULL + NECK + ids(r'cervical vertebra'), 'w': 800, 'h': 700}
# Vertebral column (left side view, front to the left of the picture)
def col(name, *pats, **kw): J[name] = {'view': 'left', 'hi': ids(*pats), 'focus': COLUMN, 'only': COLUMN + SKULL + ids(r'hip bone'), 'w': 480, 'h': 1000, 'pad': 1.05, **kw}
col('cervical', r'cervical vertebra', r'^atlas$', r'^axis$')
col('thoracic', r'thoracic vertebra')
col('lumbar', r'lumbar vertebra')
col('sacrum', r'^sacrum$')
col('discs', r'intervertebral')
up = ids(r'^atlas$', r'^axis$', r'(third|fourth) cervical')
J['atlas'] = {'view': [1, .8, .5], 'hi': ids(r'^atlas$'), 'focus': ids(r'^atlas$', r'^axis$', r'third cervical'), 'only': up, 'w': 800, 'h': 700, 'pad': 1.3}
J['axis'] = {'view': [1, .8, .5], 'hi': ids(r'^axis$'), 'focus': ids(r'^atlas$', r'^axis$', r'third cervical'), 'only': up, 'w': 800, 'h': 700, 'pad': 1.3}
J['c7'] = {'view': 'left', 'hi': ids(r'seventh cervical'), 'focus': ids(r'cervical vertebra', r'^atlas$', r'first thoracic'), 'only': COLUMN + SKULL, 'w': 700, 'h': 800, 'pad': 1.4}
# Thorax
def tho(name, *pats, **kw): J[name] = {'view': 'front', 'hi': ids(*pats), 'focus': THORAX, 'only': THORAX + COLUMN + ids(r'clavicle', r'scapula$'), 'w': 800, 'h': 800, **kw}
tho('sternum', r'^manubrium$', r'^body of sternum$', r'^xiphoid')
tho('manubrium', r'^manubrium$')
tho('xiphoid', r'^xiphoid')
tho('true-ribs', r'(first|second|third|fourth|fifth|sixth|seventh) rib$')
tho('false-ribs', r'(eighth|ninth|tenth|eleventh|twelfth) rib$')
tho('floating-ribs', r'(eleventh|twelfth) rib$', view='back')
tho('first-rib', r'first rib$')
tho('costal-cartilage', r'costal cartilage')
# Upper limb (the right one)
ARM = ids(r'right (clavicle|scapula|humerus|radius|ulna)$') + R_HAND
J['clavicle'] = {'view': 'front', 'hi': ids(r'right clavicle'), 'focus': THORAX + ids(r'clavicle', r'humerus'), 'w': 800, 'h': 800, 'only': THORAX + COLUMN + ids(r'clavicle', r'scapula$', r'humerus')}
J['scapula'] = {'view': 'back', 'hi': ids(r'right scapula'), 'focus': THORAX + ids(r'clavicle', r'humerus'), 'w': 800, 'h': 800, 'only': THORAX + COLUMN + ids(r'clavicle', r'scapula$', r'humerus')}
def arm(name, *pats, **kw): J[name] = {'view': 'front', 'hi': ids(*pats), 'focus': ARM, 'only': ARM + THORAX + COLUMN + SKULL, 'w': 520, 'h': 1000, 'pad': 1.05, **kw}
arm('humerus', r'right humerus')
arm('radius', r'right radius')
arm('ulna', r'right ulna$')
HAND_V = dict(view='front', focus=R_HAND, only=ARM, w=700, h=900, pad=1.08)
def hand(name, *pats, **kw): J[name] = {**HAND_V, 'hi': ids(*pats), **kw}
for b in ['scaphoid', 'lunate', 'triquetral', 'pisiform', 'trapezium', 'trapezoid', 'capitate', 'hamate']:
    hand(b, r'right %s$' % b)
hand('carpals', r'right (scaphoid|lunate|triquetral|pisiform|trapezium|trapezoid|capitate|hamate)$')
hand('metacarpals', r'right \w+ metacarpal')
hand('hand-phalanges', r'phalanx of right (thumb|\w+ finger)')
# Pelvis and lower limb
PELVIS = ids(r'hip bone', r'^sacrum$')
J['hip-bone'] = {'view': 'front', 'hi': ids(r'right hip bone'), 'focus': PELVIS, 'only': PELVIS + COLUMN + ids(r'femur'), 'w': 900, 'h': 700, 'pad': 1.2}
J['pelvis'] = {'view': 'front', 'hi': PELVIS, 'focus': PELVIS, 'only': PELVIS + COLUMN + ids(r'femur'), 'w': 900, 'h': 700, 'pad': 1.2}
LEG = ids(r'right (hip bone|femur|patella|tibia|fibula)$') + R_FOOT
def leg(name, *pats, **kw): J[name] = {'view': 'front', 'hi': ids(*pats), 'focus': LEG, 'only': LEG + ids(r'left (hip bone|femur|patella|tibia|fibula)$', r'^sacrum$'), 'w': 520, 'h': 1000, 'pad': 1.05, **kw}
leg('femur', r'right femur')
leg('patella', r'right patella')
leg('tibia', r'right tibia$')
leg('fibula', r'right fibula$')
FOOT_V = dict(view='top', up=[0, -1, 0], focus=R_FOOT, only=R_FOOT, w=700, h=900, pad=1.08)
def foot(name, *pats, **kw): J[name] = {**FOOT_V, 'hi': ids(*pats), **kw}
foot('talus', r'right talus')
J['calcaneus'] = {'view': 'right', 'hi': ids(r'right calcaneus'), 'focus': R_FOOT, 'only': R_FOOT + ids(r'right (tibia|fibula)$'), 'w': 900, 'h': 600}
foot('navicular', r'navicular bone of right')
foot('cuboid', r'right cuboid')
foot('cuneiforms', r'right \w+ cuneiform')
foot('tarsals', r'right (talus|calcaneus|cuboid bone)$', r'navicular bone of right', r'right \w+ cuneiform')
foot('metatarsals', r'right \w+ metatarsal')
foot('foot-phalanges', r'phalanx of right (big|second|third|fourth|little) toe')
for _f in ('muscles.py', 'nervous.py', 'cardio.py', 'resp.py', 'digest.py', 'urinary.py', 'repro.py', 'endo.py', 'integ.py', 'senses.py'): exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), _f)).read())
if __name__ == '__main__':
    only = sys.argv[1:]
    json.dump({k: v for k, v in J.items() if not only or k in only}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jobs.json'), 'w'))
    print(len(J), 'jobs')
