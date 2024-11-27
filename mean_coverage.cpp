#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <vector>
#include <string>
#include <iomanip>

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <input_file> <output_file>\n";
        return 1;
    }

    std::string input_file = argv[1];
    std::string output_file = argv[2];

    std::ifstream infile(input_file, std::ios::in | std::ios::binary);
    if (!infile.is_open()) {
        std::cerr << "Error: Unable to open input file.\n";
        return 1;
    }

    std::unordered_map<std::string, std::pair<long long, long long>> coverage_data; // chrom -> (total_depth, count)
    std::string line;
    std::string chrom;
    long long pos, depth;

    while (std::getline(infile, line)) {
        std::istringstream iss(line);
        if (!(iss >> chrom >> pos >> depth)) continue;

        coverage_data[chrom].first += depth; // Total depth
        coverage_data[chrom].second += 1;   // Count of positions
    }
    infile.close();

    std::ofstream outfile(output_file, std::ios::out | std::ios::binary);
    if (!outfile.is_open()) {
        std::cerr << "Error: Unable to open output file.\n";
        return 1;
    }

    for (const auto& entry : coverage_data) {
        double mean_depth = static_cast<double>(entry.second.first) / entry.second.second;
        outfile << entry.first << "\t" << std::fixed << std::setprecision(2) << mean_depth << "\n";
    }

    outfile.close();
    return 0;
}








# the C++ Code
# To compile the program, use a C++ compiler such as g++. Open your terminal and run:

# g++ -o mean_coverage mean_coverage.cpp
# This creates an executable file named mean_coverage.

# ./mean_coverage input_depth.gz output_mean.gz



