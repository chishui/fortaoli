#include "common.h"
#include <vector>
#include <string>
#include <fstream>
#include <cmath>
#include <iostream>
#include <sys/stat.h>

std::string path_join(const std::string &str1, const std::string &str2)
{
  if (str1.empty()) return str2;
  if (str1[str1.size() - 1] == PATH_DELIMITER)
  {
    return str1 + str2;
  }
  else
  {
    return str1 + PATH_DELIMITER + str2;
  }
}

std::string replace_ext(const std::string & str, const std::string & newext)
{
  size_t pos = str.rfind('.');
  if (pos == std::string::npos) return str;
  return str.substr(0, pos) + newext;
}

std::string get_filename(const std::string & str)
{
  size_t pos = str.rfind(PATH_DELIMITER);
  if (pos == std::string::npos) return "";
  return str.substr(pos + 1); 
}

std::vector<Point> get_point_from_csv(const std::string & filename)
{
  std::vector<Point> vPts;
  std::ifstream ifs;
  ifs.open(filename, std::ifstream::in);
  std::string line;
  for (int i = 0; std::getline(ifs, line); ++i) {
    if (!i) continue; // skip tag line
    size_t pos = line.find(",");
    line = line.substr(pos + 1);
    pos = line.find(",");
    Point pt(stof(line.substr(0, pos)), stof(line.substr(pos+1)));
    vPts.push_back(pt);
  }
  ifs.close();  
  return vPts;
}

std::ostream& operator<<(std::ostream& os, const Point& dt)  
{  
    os << '{' << dt.x << ',' << dt.y<<'}';  
    return os;  
}  

float two_points_distance(const Point & p1, const Point & p2)
{
  return sqrt(pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2)); 
}

std::vector<float> compute_length(const std::vector<Point> & vPts)
{
  std::vector<float> distances;
  for (size_t i = 0; i + 2 < vPts.size(); i += 2)
  {
    distances.push_back(two_points_distance(vPts[i], vPts[i+2]));
    if (i + 3 < vPts.size())
      distances.push_back(two_points_distance(vPts[i+1], vPts[i+3]));
  }
  return distances;
}

std::vector<float> compute_distance(const std::vector<Point> & vPts)
{
  std::vector<float> distances;
  for (size_t i = 1; i + 1 < vPts.size(); ++i)
  {
    Point p0 = vPts[i];
    Point p1 = vPts[i-1];
    Point p2 = vPts[i+1];
    distances.push_back((fabs((p2.y - p1.y) * p0.x +(p1.x - p2.x) * p0.y + ((p2.x * p1.y) -(p1.x * p2.y)))) / (sqrt(pow(p2.y - p1.y, 2) + pow(p1.x - p2.x, 2))));
  }
  return distances;
}

void to_csv(const std::string & name, const std::string & filename, std::string tag, const std::vector<float>& v)
{
  struct stat st;
  bool file_exist = (stat(filename.c_str(), &st) == 0);
  std::ofstream ofs;
  ofs.open(filename, std::ofstream::out | std::ofstream::app);
  if (!file_exist)
    ofs << "file," << tag <<"\n";
  for (size_t i = 0; i < v.size(); ++i)
  {
    ofs << name << "," << v[i] << "\n";
  }
  ofs.close();
}

extern "C" DLL_PUBLIC void compute(const char * pszfilename, const char * in_output_folder)
{
  std::string filename(pszfilename);
  std::vector<Point> vPts = get_point_from_csv(filename);
  std::vector<float> lengths = compute_length(vPts);
  std::vector<float> distances = compute_distance(vPts);
  
  std::string output_folder(in_output_folder);
  std::string name = get_filename(filename);
  to_csv(name, path_join(output_folder, get_filename(output_folder) +  "_length.csv"), "length", lengths); 
  to_csv(name, path_join(output_folder, get_filename(output_folder) +  "_dist.csv"), "dist", lengths); 
}


