let arr = [
    {
    Object: "Office Paper",
    Quantity: "0",
    Price: "10"
},
    {
    Object: "Newspaper",
    Quantity: "0",
    Price: "13"
},
    {
    Object: "Copies/Books",
    Quantity: "0",
    Price: "10"
},
{
    Object: "Cardboard",
    Quantity: "0",
    Price: "8"
},
    {
        Object: "Plastic",
    Quantity: "0",
    Price: "27"
},
    {
    Object: "Iron",
    Quantity: "0",
    Price: "37"
},
    {
    Object: "Steel Utensils",
    Quantity: "0",
    Price: "105"
},
    {
    Object: "Aluminium",
    Quantity: "0",
    Price: "105"
},
]


let s=0

for (let i = 0; i < arr.length; i++) {
    const e = arr[i];
    let a=document.getElementsByTagName("button")[i]
    let b=document.getElementsByTagName("input")[i]
    

    a.addEventListener("click",() => {
      
        if (a.innerHTML=="Add Item"){
            if (b.value=="" || b.value==0){
                alert("Please give some value of object to add")
            }
            else{
        // let q=prompt("Enter the amount of object")
        document.querySelector(".tbody").innerHTML=document.querySelector(".tbody").innerHTML+`<tr class=tr${i}>
                                                     <td>${e.Object}</td>
                                                    <td>${b.value}kg</td>
                                                    <td>₹${b.value*e.Price}</td>
                                                    </tr> `
                      a.style.backgroundColor="red"
                       a.innerHTML="Remove Item"  
          s =s+ b.value*e.Price
            document.getElementById("total").innerHTML="₹"+parseInt(s)
            document.getElementById("money").innerHTML="₹"+parseInt(s)
            
        }}
        else{
           
                          let d= document.querySelectorAll(`.tr${i}`)
                          d.forEach(e => {
                            e.innerHTML=""
                          });
                              a.style.backgroundColor="#90EE90"
                              a.innerHTML="Add Item" 
                              
                              console.log(b.value)
                              s=s - `${b.value*e.Price}`  
                              console.log(s)
                              document.getElementById("total").innerHTML="₹"+ `${s}` 
                              document.getElementById("money").innerHTML="₹"+parseInt(s)      
                            }
                        }
                        
                        
                    
                    )
}
