# Picture jobs for the special senses chapter, read by jobs.py: the eyeball, ear and nasal cartilages drawn see-through over
# the skull, with one part in red. BodyParts3D has no eyelids, lens, retina, inner ear, ossicles or tongue, so those are
# text questions; the optic nerves come from the nervous chapter.
HEAD_BONES = ids(r'frontal bone', r'parietal bone', r'temporal bone', r'occipital bone', r'sphenoid', r'ethmoid', r'maxilla', r'zygomatic', r'nasal bone', r'lacrimal', r'palatine', r'vomer', r'mandible', r'nasal concha', r'^atlas', r'^axis')
SENSE = ids(r'^eyeball$', r'^ear$', r'set of nasal cartilages', r'nasalis$', r'set of eyebrows')
def sn(name, *pats, view='front', focus=None, extra=(), xray=True, pad=1.2, w=800, h=800, **kw):
    J[name] = {'view': view, 'hi': ids(*pats), 'focus': focus or SENSE, 'only': HEAD_BONES + ids(*extra) + ids(*pats), 'xray': xray, 'w': w, 'h': h, 'pad': pad, **kw}
sn('s-eyes', r'^eyeball$', focus=ids(r'^eyeball$'), extra=(r'^eyeball$',), pad=2.0)
sn('s-eye-side', r'^eyeball$', focus=ids(r'^eyeball$', r'frontal bone'), extra=(r'^eyeball$',), view='left', pad=2.2)
sn('s-ear', r'^ear$', focus=ids(r'^ear$'), view='left', pad=2.0)
sn('s-nose', r'set of nasal cartilages', focus=ids(r'set of nasal cartilages'), extra=(r'set of nasal cartilages',), pad=2.0)
sn('s-nose-side', r'set of nasal cartilages', focus=ids(r'set of nasal cartilages'), extra=(r'set of nasal cartilages',), view='left', pad=2.0)
