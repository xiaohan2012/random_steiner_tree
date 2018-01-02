// "sampling&cut" algorithm for random steiner tree sampling
// adapted from http://www.boost.org/doc/libs/1_65_1/boost/graph/random_spanning_tree.hpp

//  Authors: Han Xiao


#ifndef BOOST_GRAPH_CUT_RANDOM_STEINER_TREE_HPP
#define BOOST_GRAPH_CUT_RANDOM_STEINER_TREE_HPP

#include <iostream>
#include <vector>

#include <boost/assert.hpp>
#include <boost/graph/loop_erased_random_walk.hpp>
#include <boost/graph/random.hpp>
#include <boost/graph/iteration_macros.hpp>
#include <boost/property_map/property_map.hpp>
#include <boost/config.hpp>
#include <boost/graph/graph_traits.hpp>
#include <boost/graph/graph_concepts.hpp>
#include <boost/graph/properties.hpp>
#include <boost/graph/named_function_params.hpp>

#include <boost/graph/random_spanning_tree.hpp>

namespace boost {

  namespace detail {
    // Use Wilson's algorithm (based on loop-free random walks) to generate a
    // random spanning tree.  The distribution of edges used is controlled by
    // the next_edge() function, so this version allows either weighted or
    // unweighted selection of trees.
    // Algorithm is from http://en.wikipedia.org/wiki/Uniform_spanning_tree
    
    template <typename Graph, typename PredMap, typename ColorMap, typename NextEdge>
    void cut_based_random_steiner_tree_internal(const Graph& g,
						std::vector<typename graph_traits<Graph>::vertex_descriptor> X, 
						typename graph_traits<Graph>::vertex_descriptor s,       
						PredMap pred,
						ColorMap color,
						NextEdge next_edge){

      random_spanning_tree_internal(g, s, pred, color, next_edge);
      // std::cout << "spanning tree built" << std::endl;

      // cut the tree 
      // traverse from terminals to the root and mark visited nodes
      std::vector<bool> visited(num_vertices(g), false);
      visited[s] = true;

      for(auto x: X){
	// std::cout << "x=" << x <<  std::endl;
	visited[x] = true;
	while(get(pred, x) != graph_traits<Graph>::null_vertex() // not root
	      && !visited[get(pred, x)]){
	  visited[get(pred, x)] = true;
	  x = get(pred, x);
	}
      }

      // std::cout << "traversing done" << std::endl;
      // remove unvisited nodes
      for(unsigned int v=0; v<num_vertices(g); v++){
      // BGL_FORALL_VERTICES_T(v, g, Graph) {
	if(!visited[v])
	  put(pred, v, graph_traits<Graph>::null_vertex());
      }
      // std::cout << "masking done" << std::endl;
    }
  }

  template <typename Graph, typename Gen, typename PredMap, typename ColorMap>
  void cut_based_random_steiner_tree(const Graph& g,
  			   std::vector<typename graph_traits<Graph>::vertex_descriptor> X,
  			   Gen& gen,
  			   typename graph_traits<Graph>::vertex_descriptor root,
  			   PredMap pred,
  			   static_property_map<double>,
  			   ColorMap color) {
    unweighted_random_out_edge_gen<Graph, Gen> random_oe(gen);
    detail::cut_based_random_steiner_tree_internal(g, X, root, pred, color, random_oe);
  }

  // Compute a weight-distributed spanning tree on a graph.
  template <typename Graph, typename Gen, typename PredMap, typename WeightMap, typename ColorMap>
  void cut_based_random_steiner_tree(const Graph& g,
			   std::vector<typename graph_traits<Graph>::vertex_descriptor> X,
			   Gen& gen,
			   typename graph_traits<Graph>::vertex_descriptor root,
			   PredMap pred,
			   WeightMap weight,
			   ColorMap color) {
    weighted_random_out_edge_gen<Graph, WeightMap, Gen> random_oe(weight, gen);
    detail::cut_based_random_steiner_tree_internal(g, X, root, pred, color, random_oe);
  }

  template <typename Graph, typename Gen, typename P, typename T, typename R>
  void cut_based_random_steiner_tree(const Graph& g,
  			   std::vector<typename graph_traits<Graph>::vertex_descriptor> X,
  			   Gen& gen, const bgl_named_params<P, T, R>& params) {
    using namespace boost::graph::keywords;
    typedef bgl_named_params<P, T, R> params_type;
    BOOST_GRAPH_DECLARE_CONVERTED_PARAMETERS(params_type, params)
    cut_based_random_steiner_tree(g,
				  X, 
				  gen,
				  arg_pack[_root_vertex | *vertices(g).first],
				  arg_pack[_predecessor_map],
				  arg_pack[_weight_map | static_property_map<double>(1.)],
				  boost::detail::make_color_map_from_arg_pack(g, arg_pack));
  }
}

#include <boost/graph/iteration_macros_undef.hpp>

#endif // BOOST_GRAPH_RANDOM_STEINER_TREE_HPP
