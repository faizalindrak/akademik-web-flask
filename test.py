from web import db
from web.models import Makul, Dosen, makul_dosen

data_dosen = db.session.query(Dosen).join(makul_dosen).all()

Dosen1 = Dosen(dosen_id=1)
mk1 = Makul(makul_id=1)

for x in Dosen1.subjects:
    print (x.nama_mk)
        
for y in mk1.lecturers:
    print (x.nama_dosen)