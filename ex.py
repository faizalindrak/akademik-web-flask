products_tags_table=db.Table('products_tags',
                    db.Column('product_id', db.Integer,db.ForeignKey('products.id'), nullable=False),
                    db.Column('tag_id',db.Integer,db.ForeignKey('tags.id'),nullable=False), 
                                                                   #^Missing 's'
                    db.PrimaryKeyConstraint('product_id', 'tag_id')
                    )

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column( db.Integer, primary_key = True)
    name = db.Column( db.String(256) )
    description = db.Column( db.Text() )
    background_img_url = db.Column( db.String(256) )
    products =db.relationship('Product',
                              secondary=products_tags_table,
                              backref='product_tags'
                             )  




class Product(db.Model):
    __tablename__ = "products"
    id = db.Column( db.Integer, primary_key = True)
    name = db.Column( db.String(256) )
    tags=db.relationship('Tag', # 'ProductTag' <- This is a relationship to the Tag table.
                    secondary=products_tags_table,
                    backref='tag_products'
                    )  