// Trying stuff out with Rust - Generates a calculator menu from the terminal

use std::io::stdin;
use std::process::exit;
use rust_tests::menu as menu;
use rust_tests::calculations as calculations;
use rust_tests::calculations::Symbol;
use rust_tests::calculations::Symbol::*;
use rust_tests::menu::Menu;

fn gen_equation(x1: i32, symbol: Symbol, x2: i32) {
    let mut equation = calculations::Equation::new(x1, symbol, x2);
    equation.get_total();
    equation.show_total();
}

fn get_input() -> String {
    let mut input_string = String::new();
    stdin().read_line(&mut input_string)
        .ok()
        .expect("Failed to read line");
    input_string.to_string()
}

fn gen_enum_value(n: &i32) -> Symbol {
    let symbol = match n {
        1 => Symbol::Division,
        2 => Symbol::Multiply,
        3 => Symbol::Subtraction,
        4 => Symbol::Addition,
        _ => Symbol::Addition,
    };
    symbol
}

fn main() {

    let mut menu: Menu = Menu::new();
    menu.create_menu(); // don't know how to trigger this from the constructor yet

    let mut i: usize = 0;
    let mut arg1: i32 = 0;
    let mut arg2: Symbol = Symbol::Addition;
    let mut arg3: i32 = 0;

    loop {
        println!("{}",menu.options[i]);
        let mut input: String = get_input();

        if input == "q".to_string().trim() {
            break;
        } else if i == 0 {
            arg1 = input.trim().parse::<i32>().unwrap();
            i+=1;
        } else if i == 1 {
            arg2 = gen_enum_value(&input.trim().parse::<i32>().unwrap());
            i+=1;
        } else {
            arg3 = input.trim().parse::<i32>().unwrap();
            break;
        }
    }

    gen_equation(arg1,arg2,arg3);

}
