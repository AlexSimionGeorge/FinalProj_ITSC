import tkinter as tk

# name holders
abi_names = [
    "zero",  # x0
    "ra",    # x1
    "sp",    # x2
    "gp",    # x3
    "tp",    # x4
    "t0",    # x5
    "t1",    # x6
    "t2",    # x7
    "s0/fp", # x8
    "s1",    # x9
    "a0",    # x10
    "a1",    # x11
    "a2",    # x12
    "a3",    # x13
    "a4",    # x14
    "a5",    # x15
    "a6",    # x16
    "a7",    # x17
    "s2",    # x18
    "s3",    # x19
    "s4",    # x20
    "s5",    # x21
    "s6",    # x22
    "s7",    # x23
    "s8",    # x24
    "s9",    # x25
    "s10",   # x26
    "s11",   # x27
    "t3",    # x28
    "t4",    # x29
    "t5",    # x30
    "t6"     # x31
]

x_registers = [0] * 32
memory = [[0] * 10 for _ in range(37)]

def main():
    def set_row_column(memory_displayed_list, row, col, val):
        memory_displayed_list[row][col].delete(0,tk.END)
        memory_displayed_list[row][col].insert(0, f"{val:5d}")

    def set_register(registers_displayed_list, x, val):
        registers_displayed_list[x].config(text= abi_names[x] + ": " + str(val))

    def execute_line_i(line_index, code_displayed_list, registers_displayed_list, memory_displayed_list):
        if line_index > 0:
            code_displayed_list[line_index - 1].config(background="white")

        #CALL BACK with data
        # execute call here set the regs and all values

        # set_row_column(memory_displayed_list, line_index, 0, 0)
        # set_register(registers_displayed_list, line_index, 9)

        code_displayed_list[line_index].config(background="red")

    def create_scrollable_frame(parent, width, height):
        canvas = tk.Canvas(parent, width=width, height=height)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return canvas, scrollable_frame

    def compile_view():
        def step_through_lines():
            nonlocal current_line
            if current_line < len(lines):
                execute_line_i(current_line, code_displayed_list, registers_displayed_list, memory_displayed_list)
                current_line += 1

        code = input_code.get(1.0, tk.END)
        lines = code.splitlines()

        ############CODE SECTION############
        code_wrapper = tk.Frame(master)
        code_wrapper.grid(row=1, column=0, padx=5, pady=5)
        # Create the scrollable code frame
        code_canvas, code_scrollable_frame = create_scrollable_frame(code_wrapper, width=350, height=850)
        # Title for the code zone
        code_zone_title = tk.Label(master, text="Code", anchor="center")
        code_zone_title.grid(row=0, column=0, padx=5, pady=5)
        # Populate the code section
        code_displayed_list = []
        for i, line in enumerate(lines):
            label = tk.Label(code_scrollable_frame, text=line, background="white", width=50, anchor="w")
            label.grid(row=i, column=0, padx=5, pady=1)
            code_displayed_list.append(label)

        ############REGISTERS SECTION############
        register_wrapper = tk.Frame(master)
        register_wrapper.grid(row=1, column=1)
        # Create the scrollable register frame
        register_canvas, register_scrollable_frame = create_scrollable_frame(register_wrapper, width=200, height=850)
        # Title for the registers zone
        registers_zone_title = tk.Label(master, text="Registers", anchor="center")
        registers_zone_title.grid(row=0, column=1, padx=5, pady=5)
        # Populate the registers section
        registers_displayed_list = []
        for i, name in enumerate(abi_names):
            label = tk.Label(register_scrollable_frame, text=name + ": " + str(x_registers[i]), background="white",
                             width=25, anchor="w")
            label.grid(row=i, column=0, padx=5, pady=1)
            registers_displayed_list.append(label)

        ############MEMORY SECTION############
        def create_memory_table(scrollable_frame, mem):
            mem_disp_list = []
            for row in range(len(mem)):  # 100 rows
                memory_address = row * len(mem[0])
                row_widgets = []

                # First column is memory address
                memory_address_label = tk.Label(scrollable_frame, text=f"{memory_address:5d}", width=7, anchor="w")
                memory_address_label.grid(row=row, column=0, padx=5, pady=1)
                # Create 10 Entry widgets for the memory values
                for col in range(len(mem[0])):
                    value = mem[row][col]
                    memory_cell = tk.Entry(scrollable_frame, width=7, justify="right")
                    memory_cell.insert(tk.END, f"{value:5d}")
                    memory_cell.grid(row=row, column=col + 1, padx=5, pady=1)
                    row_widgets.append(memory_cell)

                mem_disp_list.append(row_widgets)

            return mem_disp_list

        memory_wrapper = tk.Frame(master)
        memory_wrapper.grid(row=1, column=2, padx=5, pady=5)
        # Create the scrollable memory frame
        memory_canvas, memory_scrollable_frame = create_scrollable_frame(memory_wrapper, width=670, height=850)
        # Title for the memory zone
        memory_zone_title = tk.Label(master, text="Memory", anchor="center")
        memory_zone_title.grid(row=0, column=2, columnspan=2, padx=5, pady=5)
        # Populate the memory section with Entry widgets for a table
        memory_displayed_list = create_memory_table(memory_scrollable_frame, memory)


        # Step button
        step_button = tk.Button(master, text="Step", command=step_through_lines)
        step_button.grid(row=len(lines) + 2, column=0, pady=10)
        current_line = 0



    def swap_to_compile_view():
        input_code.pack_forget()
        run_button.pack_forget()
        compile_view()

    def input_view():
        input_code.pack()
        run_button.pack()

    # Main window setup
    master = tk.Tk()
    master.title("RISK Simulator")
    master.geometry('1920x1080')

    # Widget definitions
    input_code = tk.Text(master, height=50, width=100)
    run_button = tk.Button(master, text="Run", command=swap_to_compile_view)
    input_view()

    master.mainloop()

if __name__ == "__main__":
    main()
