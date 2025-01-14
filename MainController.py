import tkinter as tk
from Assembler import assemble_code, abi_names
from unpacker import decode_and_execute_instruction

current_line = 0
previous_line = None
initial_index_mapped_to_memory = dict()

mem = {(line, column): 0 for line in range(37) for column in range(10)}
reg = {f"x{i}": 0 for i in range(32)}

abi_names_display = list(abi_names.keys())

def main():
    def set_row_column(memory_displayed_list, row, col, val):
        memory_displayed_list[row][col].delete(0,tk.END)
        memory_displayed_list[row][col].insert(0, f"{val:5d}")


    def set_register(registers_displayed_list, x, val):
        registers_displayed_list[x].config(text=abi_names_display[x] + ": " + str(val))

    def execute_line_i(line_index, code_displayed_list, registers_displayed_list, memory_displayed_list, previous_line_loc):
        if previous_line_loc is not None:
            code_displayed_list[previous_line_loc].config(background="white")

        print("main controller", line_index)
        code_displayed_list[line_index].config(background="red")

        global mem
        global reg
        mem, reg = decode_and_execute_instruction(mem, reg, initial_index_mapped_to_memory)

        for line in range(37):
            for column in range(10):
                set_row_column(memory_displayed_list, line, column, mem[(line, column)])

        for i in range(32):
            set_register(registers_displayed_list, i, list(reg.values())[i]) #poz value

        return line_index

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

    def process_lines(input_lines):
        result = []
        for line in input_lines.splitlines():
            before_comment = line.split(";", 1)[0] if ";" in line else line
            before_comment = before_comment.lower()
            if ";" in line:
                comment = line.split(";", 1)[1]
                result.append(before_comment + ";" + comment)
            else:
                result.append(before_comment)
        return "\n".join(result)

    def format_assembly_code(code):
        formatted_code = []
        labels = []

        for line in code.splitlines():
            stripped_line = line.strip()
            if ":" in stripped_line:
                label, operation = stripped_line.split(":", 1)
                labels.append(label.strip())
    
        if labels:
            max_label_length = max(len(label) for label in labels)
        else:
            max_label_length = 0

        for line in code.splitlines():
            stripped_line = line.strip()
            if ":" in stripped_line:
                label, operation = stripped_line.split(":", 1)
                label = label.strip()
                operation = operation.strip()            
                label_padding = " " * (max_label_length - len(label))
                formatted_code.append(label + ":" + label_padding + "\t" + operation)
            elif stripped_line.startswith("."):
                formatted_code.append(stripped_line)
            else:
                formatted_code.append(max_label_length * " " + "\t" + stripped_line)

        return "\n".join(formatted_code)

    def compile_view():
        def step_through_lines():
            global current_line
            global initial_index_mapped_to_memory
            global previous_line
            if True:
                # print("current_line:", current_line, "prev line:", previous_line)
                previous_line = execute_line_i(current_line, code_displayed_list, registers_displayed_list, memory_displayed_list, previous_line)
                current_line = reg['x3'] # adc PC care  a fost modificat

        code = input_code.get(1.0, tk.END)

        code = "\n".join(line for line in code.splitlines() if line.strip())#sterge lin goale
        code = process_lines(code)
        code = format_assembly_code(code)

        # call assembler
        global mem
        global initial_index_mapped_to_memory
        global reg
        reg, mem, initial_index_mapped_to_memory = assemble_code(code, mem, reg)
        global current_line
        current_line = reg['x3']


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
        for i, name in enumerate(abi_names_display):
            label = tk.Label(register_scrollable_frame, text=name + ": " + str(list(reg.values())[i]), background="white",
                             width=25, anchor="w")
            label.grid(row=i, column=0, padx=5, pady=1)
            registers_displayed_list.append(label)

        ############MEMORY SECTION############
        def create_memory_table(scrollable_frame, mem): # TODO: change mem variable to disct touples var
            mem_disp_list = []
            for row in range(37):  # 100 rows
                memory_address = row * 10
                row_widgets = []

                # First column is memory address
                memory_address_label = tk.Label(scrollable_frame, text=f"{memory_address:5d}", width=7, anchor="w")
                memory_address_label.grid(row=row, column=0, padx=5, pady=1)
                # Create 10 Entry widgets for the memory values
                for col in range(10):
                    value = mem[(row, col)]
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
        memory_displayed_list = create_memory_table(memory_scrollable_frame, mem)


        # Step button
        step_button = tk.Button(master, text="Step", command=step_through_lines)
        step_button.grid(row=len(lines) + 2, column=0, pady=10)


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
