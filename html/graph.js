'use strict';

var app = angular.module('archeology', ['nvd3'])
app.value('APIURL', 'http://184.173.249.58:7474/db/data/')

app.controller('graph', ['$scope', '$http', 'APIURL', function($scope, $http, APIURL){
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
      var twoId = two.data.data[0][0].metadata.id;
      $http.post(APIURL+'node/'+oneId+'/path', {
        "to": twoId,
        "max_depth": depth,
        "relationships": {
          "type": "LINKS",
          "direction": "out"
        },
        "algorithm":"shortestPath"
      }).then(function(paths){
        console.log(paths);
        alert(paths);
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
      "nodes":[],
      "links":[]
  }
}])
