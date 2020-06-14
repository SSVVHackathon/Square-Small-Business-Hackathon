const paymentForm = new SqPaymentForm({
    applicationId: 'sandbox-sq0idb-5rGTvyVsL8KdON9G0GAXWw',
    card: {elementID: 'sq-card'},
    callbacks: {
        cardNonceResponseReceived: async (errors, nonce, cardData) => {
            try {
                if(errors){
                    throw new Error('\n' + errors.map((error) => {
                        return '\tEncountered error: ${error.message}';
                    }).join('\n'));
                }

                const response = await fetch('process-payment', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ source_id: nonce })
                });

                if(!response.ok){
                    console.error(await response.json());
                    throw new Error('Error status code: ${response.status}');
                }

                const json = await response.json();

                console.log(json);
                alert('Payment completed successfully!\nCheck browser developer console for more details');
            }catch (err){
                console.error(err);
                alert('Payment failed to complete!\nCheck browser developer console for more details');

            }
        }
    }
});

paymentForm.build();

const onGetCardNonce = (event) => {
    event.preventDefault();
    paymentForm.requestCardNonce();
}