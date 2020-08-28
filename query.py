from datetime import datetime, timedelta
from dateutil.parser import parse
from web.models import User, Post, Makul, Dosen, Jadwal
from web import db
from sqlalchemy import func
import locale
locale.setlocale(locale.LC_ALL, 'id_ID')

q = db.session.query(Jadwal).join(Dosen).join(Makul).filter(Makul.semester==5).filter(func.strftime('%w',Jadwal.hari)=='1').all()
print(q)
for i in q:
    print(i.kelas)