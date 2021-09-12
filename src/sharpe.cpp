#include <iostream>
#include <vector>
#include <ctime>

std::vector<float> gen_random_weights(int vec_length){
// generates random portfolio allocation weights
    std::vector<float> weights;
    
    for(size_t i {0};i < vec_length; ++i){
        int a = std::rand() % 100 + 1;
        float b = static_cast<float>(a);
        weights.push_back(b/100.0);
    }
    float total;
    for(auto& n: weights) total+=n;
    for(size_t i {0};i < weights.size(); ++i){
        weights.at(i) = weights.at(i)/total;
    }

    return weights;
}

float get_return(std::vector<float> &weights, std::vector<float> &log_returns_means, std::vector<float> &log_returns_std){
// returns expected ROI given security weights
    float num {0.0};
    float denum {0.0};
    float sharpe {0.0};
    for(size_t i {0};i<log_returns_means.size();++i){
        num+=weights.at(i)*log_returns_means.at(i);
        denum+=weights.at(i)*log_returns_std.at(i);
    }
    sharpe = num/denum;
    return sharpe;
}

size_t optimal_portolio(std::vector<float> &sharpe_arr){
    
    size_t best_pos;
    best_pos = std::distance(sharpe_arr.begin(),std::max_element(sharpe_arr.begin(),sharpe_arr.end()));
    return best_pos;

}

std::vector<float> get_sharpe_ratios(int simulations, std::vector<float> log_returns_means,
                                    std::vector<float> log_returns_std){
    
    std::cout << "\nGetting Sharpe ratios...\n" << std::endl;
    std::vector<std::vector<float>> all_weights;
    std::vector<float> sharpe_arr;
    size_t best_pos;

    for(size_t ind {0}; ind < simulations; ++ind){
        std::vector<float> weights = gen_random_weights(log_returns_means.size());
        all_weights.push_back(weights);
        sharpe_arr.push_back(get_return(weights,log_returns_means,log_returns_std));
    }

    best_pos = optimal_portolio(sharpe_arr);

    return all_weights.at(best_pos);
}

int main(){
    
    // TESTING DATA //
    std::vector<std::string> dummy_stocks {"GLW","CTVA","CAG","CF","BSX"};
    std::vector<float> dummy_returns {100.0,0.01,0.01,23.0,0.10};
    std::vector<float> dummy_std {0.1,10.0,10.0,0.01,0.04};
    std::vector<float> portfolio {};
    // END TESTING DATA //
    
    portfolio = get_sharpe_ratios(10000000,dummy_returns,dummy_std); // 10 just a placeholder
    
    std::cout << "\nOptimal portfolio: " << std::endl;
    for(size_t i {0};i<portfolio.size();++i){
        std::cout << dummy_stocks.at(i) << ": " << portfolio.at(i) << std::endl;
    }
    
    return 0;
}