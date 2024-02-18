from database.base_database import Database


class BotDatabase(Database):

    async def add_user(self, user_id: int, name: str):
        self.c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (user_id, 'user', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', name))
        self.db.commit()
        print(f'[DB] Пользователь "{user_id}" был добавлен в базу')

    async def is_user_exists(self, user_id: int) -> bool:
        try:
            user = self.c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()[0][0]
            return True
        except:
            return False

    async def is_user_admin(self, user_id: int) -> bool:
        status = await self.get_user_status(user_id)
        if status == 'admin':
            return True
        else:
            return False

    async def is_user_howner(self, user_id: int) -> bool:
        status = await self.get_user_status(user_id)
        if status == 'howner':
            return True
        else:
            return False


    async def get_user_status(self, user_id: int):
        status = self.c.execute('SELECT status FROM users WHERE user_id = (?)', (user_id,)).fetchone()[0]
        return status

    async def update_user_contacts(self, user_id: int, contacts: str):
        self.c.execute('UPDATE users SET contacts = (?) WHERE user_id = (?)', (contacts, user_id))
        self.db.commit()

    async def update_user_date(self, user_id: int, date: str, arg: str):
        self.c.execute(f'UPDATE users SET {arg}_user_date = (?) WHERE user_id = (?)', (date, user_id))
        self.db.commit()

    async def update_user_count(self, user_id: int, count: str, arg: str):
        self.c.execute(f'UPDATE users SET {arg}_user_count = (?) WHERE user_id = (?)', (count, user_id))
        self.db.commit()

    async def update_user_children(self, user_id: int, children: str, arg: str):
        self.c.execute(f'UPDATE users SET {arg}_user_children = (?) WHERE user_id = (?)', (children, user_id))
        self.db.commit()

    async def update_user_place(self, user_id: int, place: str, arg: str):
        self.c.execute(f'UPDATE users SET {arg}_user_place = (?) WHERE user_id = (?)', (place, user_id))
        self.db.commit()

    async def update_user_time(self, user_id: int, time: str, arg: str):
        self.c.execute(f'UPDATE users SET {arg}_user_time = (?) WHERE user_id = (?)', (time, user_id))
        self.db.commit()

    async def update_user_to(self, user_id: int, to: str, arg: str):
        self.c.execute(f'UPDATE users SET {arg}_user_to = (?) WHERE user_id = (?)', (to, user_id))
        self.db.commit()



    async def get_all_places(self):
        places = self.c.execute("SELECT * FROM places").fetchall()
        return places

    async def get_user_data(self, user_id: int):
        data = self.c.execute('SELECT * FROM users WHERE user_id = (?)', (user_id,)).fetchone()
        return data

    async def add_place(self, name: str):
        self.c.execute('INSERT INTO places VALUES (?)', (name,))
        self.db.commit()

    async def set_user_admin(self, user_id: int):
        self.c.execute('UPDATE users SET status = (?) WHERE user_id = (?)', ('admin', user_id))
        self.db.commit()

    async def set_user_howner(self, user_id: int):
        self.c.execute('UPDATE users SET status = (?) WHERE user_id = (?)', ('howner', user_id))
        self.db.commit()

    async def set_user_user(self, user_id: int):
        self.c.execute('UPDATE users SET status = (?) WHERE user_id = (?)', ('user', user_id))
        self.db.commit()

    # async def get_user_status(self, user_id: int):
    #     status = self.c.execute('SELECT status FROM users WHERE user_id = (?)', (user_id,)).fetchone()[0]
    #     return status

    async def set_add_place(self, user_id: int, place: str, arg: str):
        self.c.execute(f'UPDATE users SET {arg}_add_place = (?) WHERE user_id = (?)', (place, user_id))
        self.db.commit()

    async def set_add_name(self, user_id: int, name: str, arg: str):
        self.c.execute(f'UPDATE users SET {arg}_add_name = (?) WHERE user_id = (?)', (name, user_id))
        self.db.commit()

    async def set_add_desc(self, user_id: int, desc: str, arg: str):
        self.c.execute(f'UPDATE users SET {arg}_add_desc = (?) WHERE user_id = (?)', (desc, user_id))
        self.db.commit()

    async def set_add_contacts(self, user_id: int, contacts: str, arg: str):
        self.c.execute(f'UPDATE users SET {arg}_add_contacts = (?) WHERE user_id = (?)', (contacts, user_id))
        self.db.commit()

    async def set_add_photo(self, user_id: int, path: str, arg: str):
        self.c.execute(f'UPDATE users SET {arg}_add_photo = (?) WHERE user_id = (?)', (path, user_id))
        self.db.commit()

    async def get_user_data_hotel(self, user_id: int):
        data = self.c.execute('SELECT hotel_add_place, hotel_add_name, hotel_add_desc, hotel_add_contacts, hotel_add_photo FROM users WHERE user_id = (?)', (user_id,)).fetchone()
        return data

    async def add_hotel(self, user_id: int):
        data = await self.get_user_data_hotel(user_id)
        hotel_place, hotel_name, hotel_desc, hotel_contacts, hotel_photo = data
        self.c.execute('INSERT INTO hotels VALUES (?, ?, ?, ?, ?, ?)',
                       (user_id, hotel_name, hotel_place, hotel_desc, hotel_contacts, hotel_photo))
        self.db.commit()

    async def get_place_hotels(self, place: str):
        hotels = self.c.execute('SELECT * FROM hotels WHERE place = (?)', (place,)).fetchall()
        return hotels

    async def get_hotel_data(self, user_id: int, rowid: int):
        hotel_data = self.c.execute('SELECT * FROM hotels WHERE user_id = (?) AND rowid = (?)', (user_id, rowid)).fetchone()
        return hotel_data

    async def get_user_hotels(self, user_id: int):
        hotels = self.c.execute('SELECT rowid, * FROM hotels WHERE user_id = (?)', (user_id,)).fetchall()
        return hotels

    async def get_user_banyas(self, user_id: int):
        banyas = self.c.execute('SELECT rowid, * FROM banyas WHERE user_id = (?)', (user_id,)).fetchall()
        return banyas

    async def get_place_banyas(self, place: str):
        banyas = self.c.execute('SELECT * FROM banyas WHERE place = (?)', (place,)).fetchall()
        return banyas

    async def get_user_data_banya(self, user_id: int):
        data = self.c.execute(
            'SELECT banya_add_place, banya_add_name, banya_add_desc, banya_add_contacts, banya_add_photo FROM users WHERE user_id = (?)',
            (user_id,)).fetchone()
        return data

    async def delete_hotel(self, user_id: int, name: str):
        self.c.execute('DELETE FROM hotels WHERE user_id = (?) AND name = (?)', (user_id, name))
        self.db.commit()

    async def add_banya(self, user_id: int):
        data = await self.get_user_data_banya(user_id)
        banya_place, banya_name, banya_desc, banya_contacts, banya_photo = data
        self.c.execute('INSERT INTO banyas VALUES (?, ?, ?, ?, ?, ?)',
                       (user_id, banya_name, banya_place, banya_desc, banya_contacts, banya_photo))
        self.db.commit()

    async def get_banya_data(self, user_id: int, rowid: int):
        banya_data = self.c.execute('SELECT * FROM banyas WHERE user_id = (?) AND rowid = (?)',
                                    (user_id, rowid)).fetchone()
        return banya_data

    async def get_user_transfers(self, user_id: int):
        hotels = self.c.execute('SELECT rowid, * FROM transfers WHERE user_id = (?)', (user_id,)).fetchall()
        return hotels

    async def get_place_transfers(self, place: str):
        transfers = self.c.execute('SELECT * FROM transfers WHERE place = (?)', (place,)).fetchall()
        return transfers

    async def get_user_data_transfer(self, user_id: int):
        data = self.c.execute(
            'SELECT transfer_add_place, transfer_add_name, transfer_add_desc, transfer_add_contacts, transfer_add_photo FROM users WHERE user_id = (?)',
            (user_id,)).fetchone()
        return data

    async def add_transfer(self, user_id: int):
        data = await self.get_user_data_transfer(user_id)
        place, name, desc, contacts, photo = data
        self.c.execute('INSERT INTO transfers VALUES (?, ?, ?, ?, ?, ?)',
                       (user_id, name, place, desc, contacts, photo))
        self.db.commit()

    async def delete_transfer(self, user_id: int, name: str):
        self.c.execute('DELETE FROM transfers WHERE user_id = (?) AND name = (?)', (user_id, name))
        self.db.commit()

    async def get_transfer_data(self, user_id: int, rowid: int):
        transfer_data = self.c.execute('SELECT * FROM transfers WHERE user_id = (?) AND rowid = (?)',
                                    (user_id, rowid)).fetchone()
        return transfer_data

    async def get_all_transfers(self):
        transfers = self.c.execute('SELECT rowid, * FROM transfers').fetchall()
        return transfers

    async def get_all_hotels(self):
        hotels = self.c.execute('SELECT rowid, * FROM hotels').fetchall()
        return hotels

    async def get_all_users(self):
        hotels = self.c.execute('SELECT * FROM users').fetchall()
        return hotels

    async def del_place(self, name):
        self.c.execute('DELETE FROM places WHERE place = (?)', (name,))
        self.db.commit()






bot_db = BotDatabase()