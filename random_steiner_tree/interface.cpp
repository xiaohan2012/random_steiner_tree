#include <boost/foreach.hpp>

#include <boost/python.hpp>
#include <boost/python/list.hpp>
#include <boost/python/extract.hpp>

#include <vector>
#include <algorithm>
#include <iostream>
#include <sstream>
#include <iterator>
#include <random>
#include <boost/graph/graph_traits.hpp>
#include <boost/property_map/property_map.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/random/uniform_real.hpp>
#include <boost/random/uniform_int.hpp>
#include <boost/random/random_number_generator.hpp>

#include "loop_erased.cpp"
#include "cut.cpp"


// Define a directed graph type that associates a weight with each
// edge. We store the weights using internal properties as described
// in BGL.
typedef boost::property<boost::edge_weight_t, double>       EdgeProperty;
typedef boost::adjacency_list<boost::listS,
                              boost::vecS,
                              boost::undirectedS,
                              boost::no_property,
                              EdgeProperty>                 Graph;
typedef boost::graph_traits<Graph>::vertex_descriptor       Vertex;
typedef boost::graph_traits<Graph>::edge_descriptor         Edge;

Graph build_graph(int N, boost::python::list edge_with_weights){
  long l = len(edge_with_weights);
  Graph g(N);
  for(int i=0; i<l; i++){
    boost::python::list edge = (boost::python::list)edge_with_weights[i];
    int source = boost::python::extract<int>(edge[0]);
    int target = boost::python::extract<int>(edge[1]);
    double weight = boost::python::extract<double>(edge[2]);

    add_edge(source, target, weight, g);
  }
  return g;
}

int num_vertices(Graph &g){
  return boost::num_vertices(g);
}

void isolate_vertex(Graph &g, int v){
  // to keep the nodes, remove only the adjacent edges
  Graph::out_edge_iterator eit, eend;
  std::tie(eit, eend) = boost::out_edges((Vertex) v, g);
  std::vector<Edge> edges_to_remove; // collect the edges
  std::for_each(eit, eend,
  		[&g, &edges_to_remove](Edge e)
  		{
  		  // boost::remove_edge(e, g);
  		  edges_to_remove.push_back(e);
  		});
  // for(; eit < eend; eit++)
  //   edges_to_remove.push_back(*eit);
  for(auto e: edges_to_remove)
    boost::remove_edge(e, g);
}

boost::python::list reachable_vertices(Graph &g, int pivot){
  // given pivot node, traverse from it using BFS and collect nodes that are traversed
  unsigned int N = num_vertices(g);
  std::vector<Vertex> predecessors (N, boost::graph_traits<Graph>::null_vertex());

  // predecessors.fill(-1);
  boost::breadth_first_search(g, pivot,
      boost::visitor(
		     boost::make_bfs_visitor(
					     boost::record_predecessors(boost::make_iterator_property_map(predecessors.begin(), get(boost::vertex_index, g)),
									boost::on_tree_edge{})
					     )));
  boost::python::list nodes;
  for(unsigned int i=0; i<N; i++){
    if(pivot == (int)i || predecessors[i] != boost::graph_traits<Graph>::null_vertex()) // visited
      nodes.append((int) i);
  }
  return nodes;
}

std::string graph_to_string(Graph &g){
    boost::property_map<Graph, boost::edge_weight_t>::type weights =
        get(boost::edge_weight_t(), g);
    
    // Print the graph (or rather the edges of the graph).
    std::stringstream ss;
    BOOST_FOREACH (Edge e, edges(g))
    {
      ss << "(" << boost::source(e, g) << ", "
	 << boost::target(e, g) << ")\t"
	 << get(weights, e) << "\n";
    }
  
    return ss.str();;
}

boost::python::list _vertices(Graph & g){
  boost::python::list nodes;
  std::pair<Graph::vertex_iterator,
	    Graph::vertex_iterator> vs = vertices(g);
  for(Graph::vertex_iterator it=vs.first; it<vs.second; it++)
    nodes.append((int)*it);
  return nodes;
}

boost::python::list loop_erased(Graph & g, boost::python::list terminals, int root, int seed){
  long length = len(terminals);
  std::vector<Vertex> X(length);
  for(long i=0; i<length; i++){
    int node_id = boost::python::extract<int>(terminals[i]);
    X[i] = (Vertex)node_id;
  }    
  
  std::vector<Vertex> predmap (num_vertices(g), boost::graph_traits<Graph>::null_vertex());
  std::vector<boost::default_color_type> colormap(num_vertices(g));
  boost::property_map<Graph, boost::edge_weight_t>::type weightmap = get(boost::edge_weight_t(), g);

  std::mt19937 prng { seed }; // as simple as this, fanculo!!!

  loop_erased_random_steiner_tree(g,
				  X,
				  prng,
				  (Vertex) root,
				  boost::make_iterator_property_map(predmap.begin(), get(boost::vertex_index, g)),
				  weightmap,
				  boost::make_iterator_property_map(colormap.begin(), get(boost::vertex_index, g)));
  
  boost::python::list l;
  typedef boost::graph_traits<Graph>::vertex_iterator vertex_iter;
  std::pair<vertex_iter, vertex_iter> vp;
  for (vp = boost::vertices(g); vp.first != vp.second; ++vp.first){
    Vertex target= (*vp.first);
    // store visited edges
    if(predmap[target] != boost::graph_traits<Graph>::null_vertex())
      l.append(boost::python::make_tuple((int)predmap[target], target));
  }

  // BOOST_FOREACH(Edge e, branching){
  //   int source = (int)boost::source(e, g);
  //   int target = (int)boost::target(e, g);
  //   l.append(boost::python::make_tuple(source, target));
  // }
  return l;  
}

boost::python::list cut_based(Graph & g, boost::python::list terminals, int root, int seed){
  long length = len(terminals);
  std::vector<Vertex> X(length);
  for(long i=0; i<length; i++){
    int node_id = boost::python::extract<int>(terminals[i]);
    X[i] = (Vertex)node_id;
  }    
  
  std::vector<Vertex> predmap (num_vertices(g), boost::graph_traits<Graph>::null_vertex());
  std::vector<boost::default_color_type> colormap(num_vertices(g));
  boost::property_map<Graph, boost::edge_weight_t>::type weightmap = get(boost::edge_weight_t(), g);

  std::mt19937 prng { seed }; // as simple as this, fanculo!!!

  cut_based_random_steiner_tree(g,
				X,
				prng,
				(Vertex) root,
				boost::make_iterator_property_map(predmap.begin(), get(boost::vertex_index, g)),
				weightmap,
				boost::make_iterator_property_map(colormap.begin(), get(boost::vertex_index, g)));
  
  boost::python::list l;
  typedef boost::graph_traits<Graph>::vertex_iterator vertex_iter;
  std::pair<vertex_iter, vertex_iter> vp;
  for (vp = boost::vertices(g); vp.first != vp.second; ++vp.first){
    Vertex target= (*vp.first);
    // store visited edges
    if(predmap[target] != boost::graph_traits<Graph>::null_vertex())
      l.append(boost::python::make_tuple((int)predmap[target], target));
  }
  return l;  
}


BOOST_PYTHON_MODULE(interface) {
  using namespace boost::python;

  class_<Graph>("Graph");
  def("build_graph", build_graph);
  def("graph_to_string", graph_to_string);
  def("num_vertices", num_vertices);
  def("isolate_vertex", isolate_vertex);
  def("reachable_vertices", reachable_vertices);
  def("vertices", _vertices);
  def("loop_erased", loop_erased);
  def("cut_based", cut_based);    
};
