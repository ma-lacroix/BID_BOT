
pub enum Symbol {
    Multiply,
    Division,
    Subtraction,
    Addition,
}

impl Symbol {
    fn get_y(&self, x1: &i32, x2: &i32) -> i32 {
        let total: i32 = match self {
            Symbol::Multiply => x1 * x2,
            Symbol::Division => x1 / x2,
            Symbol::Subtraction => x1 - x2,
            Symbol::Addition => x1 + x2,
        };
        total
    }
}

pub struct Equation {
    pub x1: i32,
    pub symbol: Symbol,
    pub x2: i32,
    pub y: i32,
}

impl Equation {
    pub fn new(arg1: i32, arg2: Symbol, arg3: i32) -> Self {
        Self {
            x1: arg1,
            symbol: arg2,
            x2: arg3,
            y: 0,
        }
    }
    pub fn get_total(&mut self) {
        self.y = self.symbol.get_y(&self.x1,&self.x2);
    }
    pub fn show_total(self) {
        println!("The total is: {}",self.y.to_string());
    }
}