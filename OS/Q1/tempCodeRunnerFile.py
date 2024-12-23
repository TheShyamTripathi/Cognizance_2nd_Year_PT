        clear_frame(frame)
        Label(frame, text="Plane ID:").grid(row=0, column=0)
        plane_id_entry = Entry(frame)
        plane_id_entry.grid(row=0, column=1)

        Label(frame, text="Plane Model:").grid(row=1, column=0)
        plane_model_entry = Entry(frame)
        plane_model_entry.grid(row=1, column=1)

        Label(frame, text="Total Seats:").grid(row=2, column=0)
        total_seats_entry = Entry(frame)
        total_seats_entry.grid(row=2, column=1)

        Label(frame, text="Year Manufactured:").grid(row=3, column=0)
        year_manufactured_entry = Entry(frame)
        year_manufactured_entry.grid(row=3, column=1)

        return plane_id_entry, plane_model_entry, total_seats_entry, year_manufactured_entry