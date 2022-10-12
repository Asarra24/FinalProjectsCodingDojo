from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Pick:
    db = "sportpicks"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.number = data['number']
        self.bet = data['bet']
        self.record = data['record']
        self.date = data['date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = """
        INSERT INTO picks (name, number, bet, record, date, user_id) 
        VALUES (%(name)s, %(number)s, %(bet)s, %(record)s, %(date)s, %(user_id)s)
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM picks
        ;"""
        results =  connectToMySQL(cls.db).query_db(query)
        all_picks = []
        for row in results:
            all_picks.append(cls(row))
        return all_picks
    
    @classmethod
    def get_by_id(cls,data):
        query = """
        SELECT * FROM picks WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
        UPDATE picks SET name=%(name)s, number=%(number)s, 
        bet=%(bet)s, record=%(record)s, date =%(date)s, updated_at=NOW() WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls, data):
        query = """
        DELETE FROM picks WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def allPicks(cls):
        query = """
        SELECT * FROM picks 
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        return results

    @staticmethod
    def validate_pick(pick):
        is_valid = True
        if len(pick['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters!","pick")
        if len(pick['number']) < 1:
            is_valid = False
            flash("Number is required!","pick")
        if len(pick['bet']) < 1:
            is_valid = False
            flash("Bet-Size is required!","pick")    
        if pick['date'] == "":
            is_valid = False
            flash("Date is required!", "pick")
        return is_valid