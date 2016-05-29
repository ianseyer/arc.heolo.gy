'use strict';

var app = angular.module('archeology', ['nvd3'])
app.value('APIURL', 'http://184.173.249.58:7474/db/data/')

app.controller('graph', ['$scope', '$http', 'APIURL', function($scope, $http, APIURL){
  var nodes = []
  var relationships = []
  $http.post(APIURL+'cypher', {
    "query":"MATCH (n:Article {lowerTitle: {title}}) RETURN n",
    "params":{"title":"quantum mechanics"}
  }).then(function(one){
    console.log(one.data.data[0][0].metadata.id);
    $http.post(APIURL+'cypher', {
      "query":"MATCH (n:Article {lowerTitle: {title}}) RETURN n",
      "params":{"title":"poland"}
    }).then(function(two){
      var oneId = one.data.data[0][0].metadata.id;
      var twoHref = two.data.data[0][0].self;
      $http.post(APIURL+'node/'+oneId+'/paths', {
        "to": twoHref,
        "max_depth": 4,
        "relationships": {
          "type": "LINKS",
          "direction": "out"
        },
        "algorithm":"shortestPath"
      }).then(function(paths){
        paths.data.forEach(function(path, index, array){
          value.nodes.forEach(function(node, index, array){
            nodes.append($http.get(node))
            // relationships.append({"source":})
          })
        })
      })
    })
  })

  var color = d3.scale.category20()
  $scope.options = {
      chart: {
          type: 'forceDirectedGraph',
          height: (function(){ return nv.utils.windowSize().height})(),
           width: (function(){ return nv.utils.windowSize().width})(),
          margin:{top: 20, right: 20, bottom: 20, left: 20},
          color: function(d){
              return color(d.group)
          },
          nodeExtras: function(node) {
              node && node
                .append("text")
                .attr("dx", 8)
                .attr("dy", ".35em")
                .text(function(d) { return d.name })
                .style('font-size', '10px');
          }
      }
  };

  $scope.data = {
      "nodes":nodes,
      "links":[]
  }
}])
