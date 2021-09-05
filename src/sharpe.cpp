#include <iostream>
#include <vector>
#include <string>

std::vector<float> gen_random_weights(int simulations){
    
    std::vector<float> weights;
    srand((unsigned)time(NULL));
    
    for(size_t i {0};i < simulations; ++i){
        int a = std::rand() % 100 + 1;
        float b = static_cast<float>(a);
        weights.push_back(b/100.0);
    }
    float total;
    for(auto& n: weights) total+=n;
    for(size_t i {0};i < weights.size(); ++i){
        weights.at(i) = weights.at(i)/total;
        std::cout << weights.at(i) << std::endl;
    }

    return weights;
}

std::vector<float> get_sharpe_ratios(int simulations){
    /* PYTHON 
    print("\nGetting Sharpe ratios...\n")
    all_weights = np.zeros((simulations,len(df.columns)))
    ret_arr = np.zeros(simulations)
    vol_arr = np.zeros(simulations)
    sharpe_arr = np.zeros(simulations)

    for ind in range(simulations):
        weights = np.array(np.random.random(len(df.columns)))
        weights = weights / np.sum(weights)
        all_weights[ind,:] = weights
        ret_arr[ind] = np.sum((df.mean() * weights) *len(df))
        vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(df.cov() * len(df), weights)))
        sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]
    return np.round(all_weights[sharpe_arr.argmax(),:],3)
    */
    std::cout << "\nGetting Sharpe ratios...\n" << std::endl;
    std::vector<std::vector<float>> all_weights;
    std::vector<float> ret_arr;
    std::vector<float> vol_arr;
    std::vector<float> sharpe_arr;

    for(size_t ind {0}; ind < simulations; ++ind){
        std::vector<float> weights = gen_random_weights(simulations);
        all_weights.push_back(weights);
        ret_arr;
        vol_arr;
        sharpe_arr;
    }

    return sharpe_arr;

}

int main(){
    get_sharpe_ratios(10); // 10 just a placeholder
    return 0;
}