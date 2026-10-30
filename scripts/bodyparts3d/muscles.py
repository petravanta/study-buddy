# Picture jobs for the muscular chapter, read by jobs.py: the skeleton with its muscles, one muscle (or group) in red.
# `peel` takes muscles off to show a deeper one; `alone` draws only the bones and the red muscle.
MU = dict(only=ALL + MUSCLES)
def m(name, region, *pats, peel=(), alone=False, **kw):
    r = dict(REGIONS[region]); keep = set(r.pop('keep', ALL + MUSCLES)); drop = set(r.pop('drop', []))
    hi = ids(*pats); off = set(ids(*peel)) if peel else set()
    only = ALL + hi if alone else [i for i in ALL + MUSCLES if i not in off]
    J[name] = {**r, 'hi': hi, 'only': [i for i in only if i in keep and i not in drop], **kw}
HEAD_B = SKULL + NECK + ids(r'cervical vertebra', r'clavicle', r'^manubrium$', r'(first|second) rib$', r'scapula$')
HEAD_M = ids(r'frontalis', r'occipitalis', r'temporoparietalis', r'epicranius', r'orbicularis', r'corrugator', r'levator labii', r'zygomaticus', r'depressor', r'levator anguli', r'mentalis', r'buccinator', r'risorius', r'masseter', r'\btemporalis', r'pterygoid', r'nasalis', r'procerus', r'platysma', r'sternocleidomastoid', r'digastric', r'mylohyoid', r'geniohyoid', r'stylohyoid', r'sternohyoid', r'omohyoid', r'sternothyroid', r'thyrohyoid', r'scalenus', r'splenius', r'levator scapulae', r'trapezius', r'semispinalis capitis', r'longus c', r'thyroid cartilage', r'nasal cartilages')
TRUNK = THORAX + COLUMN + ids(r'clavicle', r'scapula$', r'hip bone', r'humerus')
ARMS = ids(r'clavicle', r'scapula$', r'humerus', r'radius', r'ulna$', r'(scaphoid|lunate|triquetral|pisiform|trapezium|trapezoid|capitate|hamate)$', r'metacarpal', r'of (left|right) (thumb|\w+ finger)', r'deltoid', r'biceps brachii', r'triceps', r'brachialis', r'coracobrachialis', r'anconeus', r'brachioradialis', r'pronator', r'supinator', r'flexor carpi', r'palmaris', r'flexor digitorum (superficialis|profundus)', r'pollicis', r'extensor carpi', r'extensor digitorum$', r'extensor digiti minimi', r'extensor indicis', r'of (left|right) hand', r'supraspinatus', r'infraspinatus', r'teres', r'subscapularis')
LIMB_R = ids(r'right (clavicle|scapula|humerus|radius|ulna)$') + R_HAND
FOREARM = ids(r'right (radius|ulna)$') + R_HAND
THIGH = ids(r'right (hip bone|femur|patella|tibia|fibula)$', r'^sacrum$')
LEG_R = ids(r'right (femur|patella|tibia|fibula)$') + R_FOOT
REGIONS = {
    'body': dict(view='front', focus=ALL, w=560, h=1000, pad=1.04),
    'head': dict(view='left', focus=SKULL + NECK + ids(r'clavicle'), keep=HEAD_B + HEAD_M, w=800, h=800, pad=1.06),
    'face': dict(view=[.35, -1, .05], focus=SKULL, keep=SKULL + NECK + HEAD_M, w=800, h=800),
    'trunk': dict(view='front', focus=TRUNK, w=800, h=900, pad=1.04),
    'back': dict(view='back', focus=TRUNK, w=800, h=900, pad=1.04),
    'arm': dict(view='front', focus=LIMB_R, w=560, h=1000, pad=1.05),
    'arm-back': dict(view='back', focus=LIMB_R, w=560, h=1000, pad=1.05),
    'forearm': dict(view='front', focus=FOREARM, w=560, h=1000, pad=1.06),
    'forearm-back': dict(view='back', focus=FOREARM, w=560, h=1000, pad=1.06),
    'hand': dict(view='front', focus=R_HAND, w=700, h=900, pad=1.08),
    'shoulder': dict(view='front', focus=ids(r'right (clavicle|scapula|humerus)$', r'^manubrium$'), w=800, h=800, pad=1.1),
    'shoulder-back': dict(view='back', focus=ids(r'right (clavicle|scapula|humerus)$', r'(first|seventh) thoracic'), w=800, h=800, pad=1.1),
    'hip': dict(view='back', focus=PELVIS + ids(r'femur'), drop=ARMS, w=900, h=800, pad=1.08),
    'pelvis': dict(view='front', focus=PELVIS + ids(r'femur', r'(first|second|third) lumbar'), drop=ARMS, w=900, h=800, pad=1.08),
    'leg': dict(drop=ARMS, view='front', focus=THIGH + R_FOOT, w=520, h=1000, pad=1.04),
    'leg-back': dict(drop=ARMS, view='back', focus=THIGH + R_FOOT, w=520, h=1000, pad=1.04),
    'leg-side': dict(drop=ARMS, view='right', focus=THIGH + R_FOOT, w=520, h=1000, pad=1.04),
    'calf': dict(drop=ARMS, view='back', focus=LEG_R, w=520, h=1000, pad=1.04),
    'shin': dict(drop=ARMS, view='front', focus=LEG_R, w=520, h=1000, pad=1.04),
    'shin-side': dict(drop=ARMS, view='right', focus=LEG_R, w=520, h=1000, pad=1.04),
}
J['muscles-front'] = {**REGIONS['body'], **MU}
J['muscles-back'] = {**REGIONS['body'], **MU, 'view': 'back'}
# Head and neck
m('m-frontalis', 'face', r'frontalis')
m('m-orbicularis-oculi', 'face', r'orbicularis oculi')
m('m-orbicularis-oris', 'face', r'orbicularis oris')
m('m-zygomaticus-major', 'face', r'zygomaticus major')
m('m-buccinator', 'head', r'buccinator', peel=[r'masseter', r'zygomaticus', r'risorius', r'platysma', r'depressor anguli', r'levator anguli'])
m('m-masseter', 'head', r'masseter')
m('m-temporalis', 'head', r'\btemporalis', peel=[r'temporoparietalis', r'epicranius', r'frontalis', r'occipitalis'])
m('m-pterygoids', 'head', r'pterygoid', alone=True, xray=True, view=[1, -.15, -.35])
m('m-sternocleidomastoid', 'head', r'left sternocleidomastoid')
m('m-platysma', 'head', r'left platysma', view=[1, -.7, 0])
m('m-digastric', 'head', r'digastric', view=[1, -.8, -.6], peel=[r'platysma'])
m('m-scalenes', 'head', r'left scalenus', peel=[r'sternocleidomastoid', r'trapezius', r'platysma', r'omohyoid'])
m('m-splenius-capitis', 'head', r'splenius capitis', view=[.6, 1, .1], peel=[r'trapezius', r'sternocleidomastoid'])
m('m-infrahyoid', 'head', r'sternohyoid', r'omohyoid', r'sternothyroid', r'thyrohyoid', view=[1, -.8, -.2], peel=[r'sternocleidomastoid', r'platysma'])
# Trunk
m('m-pectoralis-major', 'trunk', r'pectoralis major')
m('m-pectoralis-minor', 'trunk', r'pectoralis minor', peel=[r'pectoralis major'])
m('m-serratus-anterior', 'trunk', r'right serratus anterior', view=[-1, -.5, 0], peel=[r'right pectoralis major', r'right latissimus'])
m('m-subclavius', 'shoulder', r'right subclavius', peel=[r'pectoralis', r'deltoid', r'platysma'])
m('m-rectus-abdominis', 'trunk', r'rectus abdominis', peel=[r'external oblique', r'internal oblique', r'pectoralis major', r'pyramidalis'])
m('m-external-oblique', 'trunk', r'external oblique', view=[-.6, -1, 0])
m('m-internal-oblique', 'trunk', r'internal oblique', view=[-.6, -1, 0], peel=[r'external oblique'])
m('m-transversus-abdominis', 'trunk', r'transversus abdominis', view=[-.6, -1, 0], peel=[r'external oblique', r'internal oblique', r'rectus abdominis', r'pyramidalis'])
m('m-abdominal-wall', 'trunk', r'rectus abdominis', r'external oblique', view=[-.4, -1, 0])
m('m-diaphragm', 'trunk', r'diaphragm', alone=True, view=[0, -1, .25])
m('m-intercostals', 'trunk', r'external intercostal', view=[-.7, -1, 0], peel=[r'pectoralis', r'serratus anterior', r'latissimus', r'external oblique', r'internal oblique', r'rectus abdominis', r'deltoid', r'subclavius'])
m('m-trapezius', 'back', r'trapezius')
m('m-latissimus-dorsi', 'back', r'latissimus dorsi')
m('m-rhomboids', 'back', r'rhomboid', peel=[r'trapezius'])
m('m-levator-scapulae', 'back', r'levator scapulae', peel=[r'trapezius', r'sternocleidomastoid', r'splenius'])
m('m-erector-spinae', 'back', r'iliocostalis', r'longissimus', r'spinalis (thoracis|cervicis)', peel=[r'trapezius', r'latissimus', r'rhomboid', r'serratus posterior', r'levator scapulae', r'splenius', r'gluteus maximus', r'deltoid', r'teres', r'infraspinatus', r'supraspinatus'])
m('m-quadratus-lumborum', 'pelvis', r'quadratus lumborum', alone=True, view='back')
m('m-iliopsoas', 'pelvis', r'psoas major', r'iliacus', alone=True)
m('m-pelvic-floor', 'pelvis', r'pubococcygeus', r'puborectalis', r'iliococcygeus', r'coccygeus', alone=True, view=[0, -.5, 1], up=[0, 1, 0])
# Shoulder and arm (the right one)
m('m-deltoid', 'shoulder', r'right deltoid', view=[-1, -.8, 0])
m('m-supraspinatus', 'shoulder-back', r'right supraspinatus', peel=[r'trapezius', r'deltoid'])
m('m-infraspinatus', 'shoulder-back', r'right infraspinatus', peel=[r'trapezius', r'deltoid'])
m('m-teres-minor', 'shoulder-back', r'right teres minor', peel=[r'trapezius', r'deltoid'])
m('m-teres-major', 'shoulder-back', r'right teres major', peel=[r'deltoid'])
m('m-subscapularis', 'shoulder', r'right subscapularis', alone=True, view=[-.3, -1, 0])
m('m-rotator-cuff', 'shoulder-back', r'right (supraspinatus|infraspinatus|teres minor|subscapularis)', alone=True, view=[-.6, 1, .3])
m('m-biceps-brachii', 'arm', r'right biceps brachii')
m('m-brachialis', 'arm', r'right brachialis', peel=[r'right biceps brachii'])
m('m-coracobrachialis', 'arm', r'right coracobrachialis', peel=[r'right pectoralis', r'right deltoid', r'right biceps brachii', r'right latissimus'])
m('m-triceps-brachii', 'arm-back', r'right triceps')
m('m-anconeus', 'arm-back', r'right anconeus')
m('m-brachioradialis', 'arm', r'right brachioradialis')
# Forearm and hand
m('m-pronator-teres', 'forearm', r'right pronator teres')
m('m-flexor-carpi-radialis', 'forearm', r'right flexor carpi radialis')
m('m-palmaris-longus', 'forearm', r'right palmaris longus')
m('m-flexor-carpi-ulnaris', 'forearm', r'right flexor carpi ulnaris')
m('m-fds', 'forearm', r'right flexor digitorum superficialis', peel=[r'right (flexor carpi|palmaris|pronator teres|brachioradialis)'])
m('m-fdp', 'forearm', r'right flexor digitorum profundus', peel=[r'right (flexor carpi|palmaris|pronator teres|brachioradialis|flexor digitorum superficialis)'])
m('m-pronator-quadratus', 'forearm', r'right pronator quadratus', alone=True)
m('m-supinator', 'forearm', r'right supinator', alone=True, view=[-1, -.3, 0])
m('m-extensor-digitorum', 'forearm-back', r'right extensor digitorum$')
m('m-extensor-carpi-radialis', 'forearm-back', r'right extensor carpi radialis', view=[-1, .6, 0])
m('m-extensor-carpi-ulnaris', 'forearm-back', r'right extensor carpi ulnaris')
m('m-thumb-outcroppers', 'forearm-back', r'right (abductor pollicis longus|extensor pollicis)', view=[-1, .6, 0])
m('m-thenar', 'hand', r'right (abductor pollicis brevis|opponens pollicis|flexor pollicis brevis)')
m('m-hypothenar', 'hand', r'digiti minimi of right hand')
m('m-lumbricals', 'hand', r'lumbricals of right hand', peel=[r'right flexor digitorum'])
m('m-dorsal-interossei', 'hand', r'dorsal interossei of right hand', view='back')
# Hip and thigh (the right one)
m('m-gluteus-maximus', 'hip', r'gluteus maximus')
m('m-gluteus-medius', 'hip', r'gluteus medius', peel=[r'gluteus maximus'])
m('m-gluteus-minimus', 'hip', r'gluteus minimus', peel=[r'gluteus maximus', r'gluteus medius', r'piriformis'])
m('m-piriformis', 'hip', r'piriformis', peel=[r'gluteus maximus'])
m('m-tensor-fasciae-latae', 'leg', r'right tensor fasciae latae', view=[-1, -.7, 0])
m('m-iliotibial-tract', 'leg-side', r'right iliotibial tract')
m('m-sartorius', 'leg', r'right sartorius')
m('m-rectus-femoris', 'leg', r'right rectus femoris')
m('m-vastus-lateralis', 'leg', r'right vastus lateralis', view=[-.6, -1, 0])
m('m-vastus-medialis', 'leg', r'right vastus medialis')
m('m-vastus-intermedius', 'leg', r'right vastus intermedius', peel=[r'right rectus femoris', r'right sartorius'])
m('m-quadriceps', 'leg', r'right (rectus femoris|vastus)')
m('m-adductor-longus', 'leg', r'right adductor longus', view=[.4, -1, 0])
m('m-adductor-magnus', 'leg-back', r'right adductor magnus')
m('m-gracilis', 'leg', r'right gracilis', view=[.6, -1, 0])
m('m-pectineus', 'leg', r'right pectineus', view=[.3, -1, 0])
m('m-biceps-femoris', 'leg-back', r'right biceps femoris')
m('m-semitendinosus', 'leg-back', r'right semitendinosus')
m('m-semimembranosus', 'leg-back', r'right semimembranosus')
m('m-hamstrings', 'leg-back', r'right (biceps femoris|semitendinosus|semimembranosus)')
# Leg and foot
m('m-gastrocnemius', 'calf', r'right gastrocnemius')
m('m-soleus', 'calf', r'right soleus', peel=[r'right gastrocnemius', r'right plantaris'])
m('m-calcaneal-tendon', 'calf', r'right calcaneal tendon')
m('m-plantaris', 'calf', r'right plantaris', peel=[r'right gastrocnemius'])
m('m-popliteus', 'calf', r'right popliteus', peel=[r'right gastrocnemius', r'right plantaris', r'right (semi|biceps femoris)'])
m('m-tibialis-posterior', 'calf', r'right tibialis posterior', alone=True)
m('m-tibialis-anterior', 'shin', r'right tibialis anterior')
m('m-extensor-digitorum-longus', 'shin', r'right extensor digitorum longus', view=[-.5, -1, 0])
m('m-extensor-hallucis-longus', 'shin', r'right extensor hallucis longus')
m('m-fibularis-longus', 'shin-side', r'right fibularis longus')
m('m-fibularis-brevis', 'shin-side', r'right fibularis brevis', peel=[r'right fibularis longus'])
m('m-abductor-hallucis', 'shin-side', r'right abductor hallucis', view=[1, 0, -.2], focus=R_FOOT, w=900, h=600)
m('m-flexor-digitorum-brevis', 'shin', r'right flexor digitorum brevis', view='bottom', up=[0, -1, 0], focus=R_FOOT, w=700, h=900)
