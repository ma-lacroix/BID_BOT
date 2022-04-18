
pub struct Menu {
    pub options: Vec<String>,
}

impl Menu {
    pub fn new() -> Self {
        Self {
            options: Vec::new(),
        }
    }
    // TODO: how do I initialize a vector from the constructor?
    pub fn create_menu(&mut self) {
        self.options.push("Enter first value".to_string());
        self.options.push("Enter operator (enter a number):\n 1. divide \n \
                            2. multiply \n 3. subtract \n 4. add".to_string());
        self.options.push("Enter second value".to_string());
    }
}