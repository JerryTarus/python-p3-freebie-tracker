from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    freebies = relationship("Freebie", backref="company")
    devs = relationship("Dev", secondary="freebies")

    def give_freebie(self, dev, item_name, value):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(freebie)
        session.commit()

    @classmethod
    def oldest_company(cls):
        return cls.query.order_by(cls.founding_year).first()

    def __repr__(self):
        return f'<Company {self.name}>'



class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    freebies = relationship("Freebie", backref="dev")
    companies = relationship("Company", secondary="freebies")

    def received_one(self, item_name):
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, dev, freebie):
        if freebie.dev == self:
            freebie.dev = dev
            session.commit()

    def __repr__(self):
        return f'<Dev {self.name}>'


    
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())
    dev_id = Column(Integer(), ForeignKey("devs.id"))
    company_id = Column(Integer(), ForeignKey("companies.id"))

    dev = relationship("Dev", backref="freebies")
    company = relationship("Company", backref="freebies")

    def _dev_name(self):
        return self.dev.name if self.dev else None

    def _company_name(self):
        return self.company.name if self.company else None

    def print_details(self):
        dev_name = self._dev_name()
        company_name = self._company_name()
        return f"{dev_name} owns a {self.item_name} from {company_name}."


