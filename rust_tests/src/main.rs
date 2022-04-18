// Trying stuff out with Rust - Generates a calculator menu from the terminal

use std::io::stdin;
use std::process::exit;
use rust_tests::calculations as calculations;
use rust_tests::calculations::Symbol::*;

fn gen_equation(x1: i32, symbol: calculations::Symbol, x2: i32) {
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

fn main() {
    // TODO: write a proper menu here
    loop {
        let mut input: String = get_input();
        if input.trim() != "q".to_string() {    // trim() is to remove the line break!
            println!("Input: {}",input)
        } else {
            println!("Input: {}",input)
            break;
        }
    }

    // let x1: i32 = 30;
    // let symbol: calculations::Symbol = Subtraction;
    // let x2: i32 = 40;
    // gen_equation(x1,symbol,x2);

}
